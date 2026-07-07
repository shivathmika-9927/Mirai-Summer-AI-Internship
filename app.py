import streamlit as st

# App title and description
st.title("Echo Chamber 9000")
st.write("Enter your name and message, then click Transmit.")

# Get user inputs
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

# Run only when the button is clicked
if st.button("Transmit"):

    # Check if name is empty
    if user_name.strip() == "":
        st.error("Please provide your name.")

    # Check if message is empty
    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")

    # Execute if both inputs are valid
    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )

        # Calculate estimated token usage
        total_characters = len(user_message)
        estimated_tokens = total_characters / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{estimated_tokens:.2f} tokens from our context window."
        )