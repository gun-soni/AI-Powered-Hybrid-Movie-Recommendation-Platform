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


// =========================================
// SEARCH BUTTON
// =========================================

button.addEventListener(
    "click",
    getRecommendations
);


// =========================================
// ENTER KEY
// =========================================

input.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            getRecommendations();

        }

    }
);


// =========================================
// GET RECOMMENDATIONS
// =========================================

async function getRecommendations() {

    const userQuery =
        input.value.trim();


    recommendationDiv.innerHTML = "";

    errorDiv.innerHTML = "";


    if (!userQuery) {

        errorDiv.innerText =
            "Please enter a movie or describe what you want to watch.";

        return;
    }


    loading.style.display = "block";

    button.disabled = true;

    button.innerText = "AI Searching...";


    try {

        const response =
            await fetch(
                "/recommend",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        movie: userQuery
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


        if (
            !data ||
            !Array.isArray(
                data.recommendations
            )
        ) {

            throw new Error(
                "No recommendations found."
            );
        }


        // =================================
        // SEARCHED MOVIE
        // =================================

        const searchedMovie =
            data.searched_movie;


        if (searchedMovie) {

            const searchedContainer =
                document.createElement("div");

            searchedContainer.className =
                "searched-movie";


            searchedContainer.innerHTML =
                createMovieCard(
                    searchedMovie,
                    true
                );


            recommendationDiv.appendChild(
                searchedContainer
            );

        }


        // =================================
        // TOP 10 HEADING
        // =================================

        const recommendationTitle =
            document.createElement("h2");

        recommendationTitle.className =
            "recommendation-title";

        recommendationTitle.innerText =
            "Top 10 Recommendations";


        recommendationDiv.appendChild(
            recommendationTitle
        );


        // =================================
        // RECOMMENDATIONS
        // =================================

        const recommendations =
            data.recommendations;


        for (
            const movie of recommendations
        ) {

            const cardHTML =
                createMovieCard(
                    movie,
                    false
                );


            const cardContainer =
                document.createElement("div");


            cardContainer.innerHTML =
                cardHTML;


            const card =
                cardContainer.firstElementChild;


            recommendationDiv.appendChild(
                card
            );

        }


        // Refresh history

        loadHistory();


        // =================================
        // SCROLL TO RESULTS
        // =================================

        const section =
            document.getElementById(
                "recommendationSection"
            );


        if (section) {

            section.scrollIntoView({
                behavior: "smooth"
            });

        }

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


// =========================================
// CREATE MOVIE CARD
// =========================================

function createMovieCard(
    movie,
    isSearchedMovie
) {

    const poster =
        movie.poster ||
        "assets/default-poster.jpg";


    const overview =
        movie.overview ||
        "No overview available.";


    const tmdbRating =
        movie.tmdb_rating !== null &&
        movie.tmdb_rating !== undefined
            ? movie.tmdb_rating
            : "N/A";


    const rating =
        movie.rating !== null &&
        movie.rating !== undefined
            ? movie.rating
            : "N/A";


    const releaseDate =
        movie.release_date ||
        "Unknown";


    const title =
        movie.title ||
        "Unknown Movie";


    return `

        <div
            class="movie-card ${
                isSearchedMovie
                    ? "searched-movie-card"
                    : ""
            }"
        >

            <img
                src="${poster}"
                alt="${title}"
                loading="lazy"

                onerror="
                    this.onerror=null;
                    this.src='assets/default-poster.jpg';
                "
            >


            <div class="movie-info">

                ${
                    isSearchedMovie
                        ? `
                            <span class="searched-label">
                                YOU SEARCHED FOR
                            </span>
                          `
                        : ""
                }


                <h3>
                    ${title}
                </h3>


                <p class="rating">

                    ⭐
                    ${rating}

                </p>


                <p>

                    TMDB:
                    ${tmdbRating}

                </p>


                <p>

                    📅
                    ${releaseDate}

                </p>


                <p class="overview">

                    ${overview}

                </p>


                <div class="movie-actions">

                    <button
                        class="rate-button"
                        onclick="
                            rateMovie(
                                '${escapeMovieTitle(title)}'
                            )
                        "
                    >
                        ⭐ Rate
                    </button>


                    <button
                        class="watchlist-button"
                        onclick="
                            addToWatchlist(
                                '${escapeMovieTitle(title)}'
                            )
                        "
                    >
                        ➕ Watchlist
                    </button>

                </div>

            </div>

        </div>

    `;
}


// =========================================
// ESCAPE MOVIE TITLE
// =========================================

function escapeMovieTitle(title) {

    return String(title)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'");
}


// =========================================
// RATE MOVIE
// =========================================

async function rateMovie(
    movieTitle
) {

    const rating =
        prompt(
            `Rate "${movieTitle}" from 1 to 5:`
        );


    if (rating === null) {

        return;
    }


    const numericRating =
        Number(rating);


    if (
        isNaN(numericRating) ||
        numericRating < 1 ||
        numericRating > 5
    ) {

        alert(
            "Please enter a rating between 1 and 5."
        );

        return;
    }


    try {

        const response =
            await fetch(
                "/rate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        movie_title:
                            movieTitle,

                        rating:
                            numericRating

                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not save rating."
            );
        }


        alert(
            `You rated "${movieTitle}" ${numericRating}/5`
        );

    }


    catch (error) {

        console.error(
            "Rating Error:",
            error
        );

        alert(
            error.message
        );

    }

}


// =========================================
// ADD TO WATCHLIST
// =========================================

async function addToWatchlist(
    movieTitle
) {

    try {

        const response =
            await fetch(
                "/watchlist",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        movie_title:
                            movieTitle

                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not add movie to watchlist."
            );
        }


        alert(
            `"${movieTitle}" added to your watchlist.`
        );


        loadWatchlist();

    }


    catch (error) {

        console.error(
            "Watchlist Error:",
            error
        );

        alert(
            error.message
        );

    }

}


// =========================================
// LOAD WATCHLIST
// =========================================

async function loadWatchlist() {

    const watchlistDiv =
        document.getElementById(
            "watchlistMovies"
        );


    if (!watchlistDiv) {

        return;
    }


    try {

        const response =
            await fetch(
                "/watchlist"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                "Could not load watchlist."
            );
        }


        watchlistDiv.innerHTML = "";


        if (
            !Array.isArray(data) ||
            data.length === 0
        ) {

            watchlistDiv.innerHTML =
                "<p>No movies in your watchlist yet.</p>";

            return;
        }


        for (const movie of data) {

            const title =
                movie.movie_title ||
                movie.title ||
                "Unknown Movie";


            const cardHTML =
                createMovieCard(
                    {
                        id: movie.id,

                        title: title,

                        poster:
                            movie.poster,

                        rating:
                            movie.rating,

                        tmdb_rating:
                            movie.tmdb_rating,

                        release_date:
                            movie.release_date,

                        overview:
                            movie.overview
                    },
                    false
                );


            const cardContainer =
                document.createElement("div");


            cardContainer.innerHTML =
                cardHTML;


            const card =
                cardContainer.firstElementChild;


            // Add remove cross

            const removeButton =
                document.createElement("button");


            removeButton.innerText =
                "×";


            removeButton.className =
                "watchlist-remove-button";


            removeButton.title =
                "Remove from watchlist";


            removeButton.onclick =
                function () {

                    deleteWatchlistItem(
                        movie.id
                    );

                };


            card.style.position =
                "relative";


            card.appendChild(
                removeButton
            );


            watchlistDiv.appendChild(
                card
            );

        }

    }


    catch (error) {

        console.error(
            "Watchlist Error:",
            error
        );


        watchlistDiv.innerHTML =
            "<p>Could not load watchlist.</p>";

    }

}


// =========================================
// DELETE WATCHLIST ITEM
// =========================================

async function deleteWatchlistItem(
    watchlistId
) {

    try {

        const response =
            await fetch(
                `/watchlist/${watchlistId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not remove movie from watchlist."
            );

        }


        loadWatchlist();

    }


    catch (error) {

        console.error(
            "Delete Watchlist Error:",
            error
        );


        alert(
            error.message
        );

    }

}


// =========================================
// LOAD SEARCH HISTORY
// =========================================

async function loadHistory() {

    const historyDiv =
        document.getElementById(
            "historyMovies"
        );


    if (!historyDiv) {

        return;
    }


    try {

        const response =
            await fetch(
                "/history"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                "Could not load search history."
            );
        }


        historyDiv.innerHTML = "";


        if (
            !Array.isArray(data) ||
            data.length === 0
        ) {

            historyDiv.innerHTML =
                "<p>No search history yet.</p>";

            return;
        }


        for (const movie of data) {

            const title =
                movie.movie_title ||
                movie.title ||
                "Unknown Movie";


            const historyCard =
                document.createElement("div");


            historyCard.className =
                "history-card";


            historyCard.innerHTML = `

                <span class="history-title">
                    ${title}
                </span>

                <button
                    class="history-delete-button"
                    title="Delete search"
                    onclick="
                        deleteHistoryItem(
                            ${movie.id}
                        )
                    "
                >
                    ×
                </button>

            `;


            historyDiv.appendChild(
                historyCard
            );

        }

    }


    catch (error) {

        console.error(
            "History Error:",
            error
        );


        historyDiv.innerHTML =
            "<p>Could not load search history.</p>";

    }

}


// =========================================
// DELETE HISTORY ITEM
// =========================================

async function deleteHistoryItem(
    historyId
) {

    try {

        const response =
            await fetch(
                `/history/${historyId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Could not delete search history."
            );

        }


        loadHistory();

    }


    catch (error) {

        console.error(
            "Delete History Error:",
            error
        );


        alert(
            error.message
        );

    }

}


// =========================================
// LOAD DATA WHEN PAGE OPENS
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadWatchlist();

        loadHistory();

    }
);