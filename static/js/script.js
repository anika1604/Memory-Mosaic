document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the default form submission

    const fileInput = document.getElementById("imageUpload");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);  // Send only one image file

    try {
        const response = await fetch("/upload_image", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            // Display the generated mosaic image
            document.getElementById("mosaicContainer").innerHTML = `<img src="${result.mosaic_url}" alt="Generated Mosaic">`;
        } else {
            alert("Failed to generate mosaic.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while uploading the image.");
    }
});
