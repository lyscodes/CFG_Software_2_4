function searchGifs() {
    var emotion = document.getElementById("emotion-input").value.trim();
  
    // Clear previous gifs
    document.getElementById("gif-container").innerHTML = "";
  
    // Fetch GIFs from Giphy API
    fetch(`https://api.giphy.com/v1/gifs/search?api_key=cuS52zkG2nIj9fB2YwO06L8j12KwgZKs&q=${emotion}&limit=10`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data); // Log the API response
        data.data.forEach(gif => {
          var gifUrl = gif.images.fixed_height.url;
          var img = document.createElement("img");
          img.src = gifUrl;
          img.classList.add("gif");
          
          // Add click event listener to each GIF
          // Doesn't really do anything just yet lol it just creates a pop-up.
          img.addEventListener('click', function() {
            alert('Emotion saved');
          });
  
          document.getElementById("gif-container").appendChild(img);
        });
      })
      .catch(error => console.error("Error fetching GIFs:", error));
  }
  