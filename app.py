import streamlit as st
from dotenv import load_dotenv
from backend import *
import uuid

# Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] =''

def main():
    load_dotenv()
    st.set_page_config(page_title="Resume Screening Assistance")
    st.title("HR - Resume Screening Assistance...💁 ")
    st.subheader("I can help you in resume screening process")

    job_description = st.text_area(
        "Please paste the 'JOB DESCRIPTION' here...", key="1"
    )
    document_count = st.text_input("No.of 'RESUMES' to return", key="2")
    # Upload the Resumes (pdf files)
    pdf = st.file_uploader(
        "Upload resumes here, only PDF files allowed",
        type=["pdf"],
        accept_multiple_files=True,
    )

    submit = st.button("Submit")
    if submit:
        if not job_description.strip():
            st.warning("Please enter the job description.")
            return
        if not document_count.strip().isdigit():
            st.warning("Please enter a valid number of resumes.")
            return
        if not pdf:
            st.warning("Please upload at least one PDF resume.")
            return

        with st.spinner('Wait for it...'):
            if not job_description.strip():
                st.warning("Please enter the job description.")
                return
            if not document_count.strip().isdigit():
                st.warning("Please enter a valid number of resumes.")
                return
            if not pdf:
                st.warning("Please upload at least one PDF resume.")
                return

        with st.spinner("Processing..."):
            st.session_state["unique_id"] = uuid.uuid4().hex
            docs_list = create_docs(pdf, st.session_state["unique_id"])
            st.write(f"📄 Resumes uploaded: {len(docs_list)}")

            embeddings = create_embeddings_load_data()
            push_to_pine(embeddings, docs_list)

            docs = similar_doc(
                embeddings,
                job_description,
                int(document_count),
                st.session_state["unique_id"]
            )

            st.write("➖" * 30)
            for i, (doc, score) in enumerate(docs, 1):
                st.subheader(f"👉 {i}")
                st.write(f"**File:** {doc.metadata['name']}")
                with st.expander("Show me 👀"):
                    st.info(f"**Match Score:** {score*100}")
                    st.write(f"**Summary:** {get_summary(doc)}")

        st.success("Hope I saved you some time ❤️")



if __name__ == "__main__":
    main()
