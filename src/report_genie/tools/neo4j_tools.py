from crewai.tools import tool
from neo4j import GraphDatabase
import os

## Neo4j connection details
NEO_DB_URI = os.getenv("NEO_DB_URI")
NEO_DB_USERNAME = os.getenv("NEO_DB_USERNAME")
NEO_DB_PWD = os.getenv("NEO_DB_USERNAME")
NEO_DB_DATABSE = os.getenv("NEO_DB_DATABSE")

AUTH = (NEO_DB_USERNAME, NEO_DB_PWD)
driver = GraphDatabase.driver(NEO_DB_URI, auth=AUTH)

@tool("get_city_info")
def get_city_info(city_name: str, industry_name: str) -> list:
        """
        Get various information about a city and industry

        Given a city and an industry, fetch the following information from the graph database:
        - The number of organizations in the given industry that are in the given city
        - The number of public companies in the given industry that are in the given city
        - The total revenue of all companies in the given industry that are in the given city
        - The 5 companies in the given industry that are in the given city with the most employees

        :param city_name: The name of the city
        :param industry_name: The name of the industry
        :return: A list of dictionaries, each containing the above information
        """
        data, _, _ = driver.execute_query("""MATCH (c:City)<-[:IN_CITY]-(o:Organization)-[:HAS_CATEGORY]->(i:IndustryCategory)
                    WHERE c.name = $city AND i.name = $industry
                    WITH o
                    ORDER BY o.nbrEmployees DESC
                    RETURN count(o) AS organizationCount,
                    sum(CASE WHEN o.isPublic THEN 1 ELSE 0 END) AS publicCompanies,
                    sum(o.revenue) AS combinedRevenue,
                    collect(CASE WHEN o.nbrEmployees IS NOT NULL THEN o END)[..5] AS topFiveOrganizations""", city=city_name, industry=industry_name)
        return [el.data() for el in data]


@tool("get_news")
def get_news(company: str) -> list:
        """
        Get the 5 most recent news articles mentioning a given company.

        :param company: The name of the company to search for
        :return: A list of dictionaries with the following keys:
            - title: The title of the article
            - date: The date the article was published
            - sentiment: The sentiment of the article (positive, negative, or neutral)
            - chunks: A list of strings containing the text of the article
        """
        data, _, _ = driver.execute_query("""MATCH (c:Chunk)<-[:HAS_CHUNK]-(a:Article)-[:MENTIONS]->(o:Organization)
                    WHERE o.name = $company AND a.date IS NOT NULL
                    WITH c, a
                    ORDER BY a.date DESC
                    LIMIT 5
                    RETURN a.title AS title, a.date AS date, a.sentiment AS sentiment, collect(c.text) AS chunks""", company=company)
        return [el.data() for el in data]
