document.addEventListener('DOMContentLoaded', () => {
    const recommendationDiv = document.getElementById('recommendation');
    const popularartistsDiv = document.getElementById('popular-artists');
    const searchForm = document.getElementById('search-form');



    searchForm.addEventListener('submit', async(e) => {
        e.preventDefault();
        const artist = document.getElementById('artist-search').value;
        recommendationDiv.innerHTML = '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';
        const response = await fetch(`/recommendation?artist=${encodeURIComponent(artist)}`);
        const data = await response.json();
        if (data.error) {
            recommendationDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else if (data.artist_names) {
            let content = '<div id="artist_recs" class="artist_rec-list">';
            for (let i = 0; i < data.artist_names.length; i++) {
                content += `
                    <div class="artistss" onclick="window.open('${data.spotify_profiles[i]}', '_blank')" style="cursor: pointer;" rec-artist="${data.artist_names[i]}" artist-genre="${data.genres[i]}">
                        <p class='artist-text'><strong>${data.artist_names[i]}</strong></p>
                        <p><strong>Genre:</strong> ${data.genres[i]}</p>
                        <p><img src="${data.images[i]}" alt="${data.artist_names[i]}"></p>
                    </div>
                `;
            }
            content += '</div>';
            recommendationDiv.innerHTML = content;
        } else {
            recommendationDiv.innerHTML = `<p>Check artist name</p>`;
        }

    });
});



function showDropdown() {
    let input = document.getElementById('artist-search').value;

    if (input.length >= 3) {
        fetch(`/search_suggestions?query=${input}`)
            .then(response => response.json())
            .then(suggestions => {
                let dropdown = document.getElementById('dropdownList');
                dropdown.innerHTML = '';
                suggestions.forEach(item => {
                    let button = document.createElement('button');
                    button.innerText = item;
                    button.classList.add('dropdown-item'); // Add Bootstrap class or your own class for styling
                    button.type = 'button'; // Specify the button type
                    button.onclick = function() {
                        document.getElementById('artist-search').value = item;
                        dropdown.classList.remove('show-dropdown');
                    };
                    dropdown.appendChild(button);
                });
                dropdown.classList.toggle('show-dropdown', suggestions.length > 0);
            });
    } else {
        document.getElementById('dropdownList').classList.remove('show-dropdown');
    }
}