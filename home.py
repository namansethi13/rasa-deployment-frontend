import streamlit as st
from PIL import Image
def main():
    st.set_page_config(layout="wide")

    st.title("Rasa App Deployment and Analytics")

    st.write(
        "Welcome to the Rasa App Deployment and Analytics platform! This platform allows you to easily deploy a Rasa chatbot "
        "and view it's analytics"
    )

    st.write(
        "Here, you can deploy your Rasa chatbot with just one click and also view analytics to track its performance. "
        "Select the appropriate options from the navigation menu to get started."
    )

    image = Image.open('flowchart.png')
    st.image(image)
if __name__ == "__main__":
    main()
