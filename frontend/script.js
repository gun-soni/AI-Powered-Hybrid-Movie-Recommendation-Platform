const button = document.getElementById("searchBtn");

const input = document.getElementById("movieName");

const recommendationDiv =
    document.getElementById("recommendations");

const loading =
    document.getElementById("loading");

const errorDiv =
    document.getElementById("error");


button.addEventListener("click", getRecommendations);


input.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        getRecommendations();

    }

});


async function getRecommendations() {

    const movie = input.value.trim();

    recommendationDiv.innerHTML = "";

    errorDiv.innerHTML = "";

    if (!movie) {

        errorDiv.innerText =
            "Please enter a movie name.";

        return;

    }

    loading.style.display = "block";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/recommend",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    movie: movie
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "Movie could not be found."
            );

        }


        const recommendations =
            await response.json();


        for (const movie of recommendations) {

            recommendationDiv.innerHTML += `

                <div class="movie-card">

                    <h3>${movie.title}</h3>

                    <p>
                        ⭐ ${movie.rating}
                    </p>

                    <p>
                        📅 ${movie.release_date}
                    </p>

                </div>

            `;

        }

    }

    catch (error) {

        console.error(error);

        errorDiv.innerText =
            "Unable to get recommendations.";

    }

    finally {

        loading.style.display = "none";

    }

}