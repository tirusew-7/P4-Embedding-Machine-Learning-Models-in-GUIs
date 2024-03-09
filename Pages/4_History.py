import streamlit as st

def show():
    st.title("History Page")
    # Your history page content goes here
    st.write("This is the History Page content.")
    
def show_history():
    if "history" in st.session_state:
        st.markdown("### Vodafom Churn Prediction History")
        for entry in st.session_state["history"]:
            st.markdown(f"#### Prediction made on {entry['timestamp']}")  # Assuming you have a timestamp
            st.write("**User Inputs:**")
            for key, value in entry["inputs"].items():
                st.write(f"- {key}: {value}")
            st.write("**Prediction:**")
            if entry["prediction"] == 1:
                st.write("- Customer will churn")
            else:
                st.write("- Customer will not churn")
            st.write("**Probability of Churn:**", entry["probability"])
            st.write("---")
    else:
        st.write("No previous history found.")

def main():
    show_history()

if __name__ == "__main__":
    main()
