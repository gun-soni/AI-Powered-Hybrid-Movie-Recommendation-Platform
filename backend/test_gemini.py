from services.gemini import understand_query

query = "Recommend emotional space movies like Interstellar"

result = understand_query(query)

print(result)