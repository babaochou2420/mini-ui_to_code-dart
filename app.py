import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai

# Configure the API key directly in the script
API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model name
MODEL_NAME = "gemini-1.5-pro-latest"

# Create the model
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Function to send a message to the model
def send_message_to_model(message, image_path):
    image_input = {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }
    response = chat_session.send_message([message, image_input])
    return response.text

# Streamlit app
def main():
    st.title("Gemini 1.5 Pro, UI to Code 👨‍💻 ")
    st.subheader('Made with ❤️ by [Skirano](https://x.com/skirano)')

    # Dropdown to select code generation type (HTML or Flutter)
    code_type = st.selectbox("Choose code type to generate", ["HTML", "Flutter"])

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            # Convert image to RGB mode if it has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Save the uploaded image temporarily
            temp_image_path = pathlib.Path("temp_image.jpg")
            image.save(temp_image_path, format="JPEG")

            # Generate code based on the selected type
            if st.button(f"Generate {code_type} code"):
                st.write(f"🧑‍💻 Looking at your UI for {code_type}...")

                # Generate description of the UI
                prompt = "Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)]. Also describe the color and positioning of the elements."
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)

                # Refine the description
                st.write("🔍 Refining description with visual comparison...")
                refine_prompt = f"Compare the described UI elements with the provided image and identify any missing elements or inaccuracies. Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
                refined_description = send_message_to_model(refine_prompt, temp_image_path)
                st.write(refined_description)

                if code_type == "Flutter":
                    # Generate Flutter UI code
                    st.write("🛠️ Generating Flutter UI code...")
                    flutter_prompt = f"Create a Flutter code based on the following UI description, including proper layout widgets (e.g., `Container`, `Row`, `Column`, etc.) with appropriate padding, alignment, and positioning. Use `BoxDecoration` for styling and colors to match the original UI. Ensure the code is responsive and mobile-first. Here is the refined description: {refined_description}"
                    initial_flutter_code = send_message_to_model(flutter_prompt, temp_image_path)
                    st.code(initial_flutter_code, language='dart')

                    # Refine Flutter UI code
                    st.write("🔧 Refining Flutter UI code...")
                    refine_flutter_prompt = f"Validate the following Flutter code based on the UI description and image and provide a refined version of the code that improves accuracy, responsiveness, and adherence to the original design. Here is the initial Flutter code: {initial_flutter_code}"
                    refined_flutter_code = send_message_to_model(refine_flutter_prompt, temp_image_path)
                    st.code(refined_flutter_code, language='dart')

                    # Save the refined Flutter code to a file
                    with open("flutter_ui.dart", "w") as file:
                        file.write(refined_flutter_code)
                    st.success("Flutter UI file 'flutter_ui.dart' has been created.")

                    # Provide download link for Flutter code
                    st.download_button(label="Download Flutter UI Code", data=refined_flutter_code, file_name="flutter_ui.dart", mime="application/dart")

                else:
                    # Generate HTML code
                    st.write("🛠️ Generating HTML code...")
                    html_prompt = f"Create an HTML file based on the following UI description, using flexbox and grid layout with inline CSS. Ensure the colors and layout match the original UI. Here is the refined description: {refined_description}"
                    initial_html_code = send_message_to_model(html_prompt, temp_image_path)
                    st.code(initial_html_code, language='html')

                    # Refine HTML code
                    st.write("🔧 Refining HTML code...")
                    refine_html_prompt = f"Validate the following HTML code based on the UI description and image and provide a refined version of the code that improves accuracy, responsiveness, and adherence to the original design. Here is the initial HTML code: {initial_html_code}"
                    refined_html_code = send_message_to_model(refine_html_prompt, temp_image_path)
                    st.code(refined_html_code, language='html')

                    # Save the refined HTML code to a file
                    with open("index.html", "w") as file:
                        file.write(refined_html_code)
                    st.success("HTML file 'index.html' has been created.")

                    # Provide download link for HTML code
                    st.download_button(label="Download HTML Code", data=refined_html_code, file_name="index.html", mime="text/html")

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
