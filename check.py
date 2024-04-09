import streamlit as st

def process_text(text):
    # Function to process the text and return some output
    return f"You entered: {text}"

def main():
    st.title("Text Input with Submit and Download Button")

    # Text input area
    text_input = st.text_area("Enter Text:")

    # Create two columns
    col1, col2 = st.columns([2, 1])

    # Submit button
    with col1:
        if st.button("Submit"):
            if text_input:
                output = process_text(text_input)
                # Show the output
                st.write(output)

    # Download button
    with col2:
        if text_input and st.button("Download Output"):
            output = process_text(text_input)
            st.download_button(label="Download", data=output, file_name="output.txt")

if __name__ == "__main__":
    main()
