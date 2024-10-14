const imageInput = document.getElementById("imageInput"); // upload image
const preview = document.getElementById("preview"); // Preview image
const result = document.getElementById("result"); // result from server

imageInput.addEventListener("change", (e) => {
  console.log(e.target.files[0]);
  const file = e.target.files[0]; // get selected file
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

async function sendRequest(endpoint, formData) {
  try {
    console.log(`Mengirim permintaan ke ${endpoint}`);
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
      method: "POST",
      body: formData,
    });
    console.log("Respons diterima");
    const data = await response.json();
    console.log("Data:", data);
    result.src = `data:image/jpeg;base64,${data.image_base64}`;
  } catch (error) {
    console.error("Error:", error);
    alert("Terjadi kesalahan saat memproses gambar.");
  }
}
function cropImage() {
  const formData = new FormData();
  formData.append("image_file", imageInput.files[0]);
  formData.append("x", parseInt(document.getElementById("cropX").value));
  formData.append("y", parseInt(document.getElementById("cropY").value));
  formData.append(
    "width",
    parseInt(document.getElementById("cropWidth").value)
  );
  formData.append(
    "height",
    parseInt(document.getElementById("cropHeight").value)
  );
  sendRequest("crop", formData);
}
function grayscaleImage() {
  const formData = new FormData();
  formData.append("image_file", imageInput.files[0]);
  sendRequest("grayscale", formData);
}

function convolveImage() {
  const formData = new FormData();
  formData.append("image_file", imageInput.files[0]);
  sendRequest("convolution", formData);
}
