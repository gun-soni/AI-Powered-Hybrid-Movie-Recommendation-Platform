from services.gemini import understand_query


queries = [

    "Recommend emotional sci-fi movies like Interstellar",

    "Give me funny family movies",

    "I want a Christopher Nolan movie",

    "Suggest romantic movies from 2010",

    "Give me movies similar to Titanic"

]


for query in queries:

    print("\nUSER:")
    print(query)

    result = understand_query(query)

    print("\nGEMINI:")
    print(result.model_dump())