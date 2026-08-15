const button =
    document.getElementById("searchBtn");

const input =
    document.getElementById("movieName");

const recommendationDiv =
    document.getElementById("recommendations");

const loading =
    document.getElementById("loading");

const errorDiv =
    document.getElementById("error");


button.addEventListener(
    "click",
    getRecommendations
);


input.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            getRecommendations();

        }

    }
);


async function getRecommendations() {

    const movieName =
        input.value.trim();


    recommendationDiv.innerHTML = "";

    errorDiv.innerHTML = "";


    if (!movieName) {

        errorDiv.innerText =
            "Please enter a movie name.";

        return;
    }


    loading.style.display = "block";


    button.disabled = true;

    button.innerText = "Searching...";


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/recommend",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    movie: movieName
                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to get recommendations."
            );
        }


        if (!Array.isArray(data) ||
            data.length === 0) {

            throw new Error(
                "No recommendations found."
            );
        }


        for (const movie of data) {

            const poster = movie.poster || "assets/default-poster.jpg";


            const overview =
                movie.overview ||
                "No overview available.";


            const tmdbRating =
                movie.tmdb_rating !== null &&
                movie.tmdb_rating !== undefined
                    ? movie.tmdb_rating
                    : "N/A";


            recommendationDiv.innerHTML += `

                <div class="movie-card">

                    <img
                        src="${poster}"
                        alt="${movie.title}"
                        loading="lazy"
                        onerror="this.onerror=null; this.src='assets/default-poster.jpg';"
                    >

                    <div class="movie-info">

                        <h3>
                            ${movie.title}
                        </h3>

                        <p class="rating">
                            ⭐ ${movie.rating}
                        </p>

                        <p>
                            TMDB:
                            ${tmdbRating}
                        </p>

                        <p>
                            📅
                            ${
                                movie.release_date ||
                                "Unknown"
                            }
                        </p>

                        <p class="overview">
                            ${overview}
                        </p>

                    </div>

                </div>

            `;
        }


        document
            .getElementById(
                "recommendationSection"
            )
            .scrollIntoView({
                behavior: "smooth"
            });

    }


    catch (error) {

        console.error(
            "Recommendation Error:",
            error
        );


        errorDiv.innerText =
            error.message;

    }


    finally {

        loading.style.display = "none";

        button.disabled = false;

        button.innerText = "Recommend";

    }

}