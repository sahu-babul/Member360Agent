import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Load local data
def load_data(file_name):
    try:
        with open(os.path.join("data", file_name), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Page configuration
st.set_page_config(
    page_title="Member 360 Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .member-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Member 360")
    
    # Navigation
    page = option_menu(
        menu_title=None,
        options=["Dashboard", "Member Management", "Document Intelligence", "AI Insights"],
        icons=["house", "people", "file-earmark-text", "robot"],
        default_index=0
    )
    
    # Quick Stats
    st.markdown("---")
    st.subheader("Quick Stats")
    members = load_data("members.json")
    total_members = len(members)
    active_members = len([m for m in members if m["status"] == "Active"])
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Members", total_members)
    with col2:
        st.metric("Active Members", active_members)

# Main content
if page == "Dashboard":
    st.title("📊 Member 360 Dashboard")
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Members", total_members)
    with col2:
        st.metric("Active Members", active_members)
    with col3:
        if total_members > 0:
            active_rate = (active_members/total_members)*100
            st.metric("Active Rate", f"{active_rate:.1f}%")
        else:
            st.metric("Active Rate", "0%")
    with col4:
        interactions = load_data("interactions.json")
        st.metric("Total Interactions", len(interactions))
    
    # Charts Row
    col1, col2 = st.columns(2)
    with col1:
        # Membership Type Distribution
        membership_data = pd.DataFrame(members)
        fig = px.pie(membership_data, names='membershipType', title='Membership Type Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status Distribution
        status_data = pd.DataFrame(members)
        fig = px.bar(status_data['status'].value_counts(), title='Member Status Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity
    st.subheader("📈 Recent Activity")
    interactions = load_data("interactions.json")
    if interactions:
        recent_interactions = sorted(interactions, key=lambda x: x["date"], reverse=True)[:10]
        df = pd.DataFrame(recent_interactions)
        
        # Convert date strings to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Create a timeline chart
        fig = px.timeline(df, 
                         x_start="date", 
                         x_end="date",
                         y="type",
                         color="status",
                         title="Recent Interactions Timeline")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display interactions table
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No interactions found. Run the data generation script first.")

elif page == "Member Management":
    st.title("👥 Member Management")
    
    # Search and Filter
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search Members")
    with col2:
        status_filter = st.multiselect(
            "Status",
            options=["Active", "Inactive", "Pending"],
            default=["Active"]
        )
    with col3:
        membership_filter = st.multiselect(
            "Membership Type",
            options=["Basic", "Premium", "Gold"],
            default=["Basic", "Premium", "Gold"]
        )
    
    # Display members
    members = load_data("members.json")
    if search_term:
        members = [m for m in members if search_term.lower() in m["firstName"].lower() or 
                  search_term.lower() in m["lastName"].lower() or 
                  search_term.lower() in m["email"].lower()]
    
    if status_filter:
        members = [m for m in members if m["status"] in status_filter]
    
    if membership_filter:
        members = [m for m in members if m["membershipType"] in membership_filter]
    
    if members:
        for member in members:
            with st.expander(f"{member['firstName']} {member['lastName']} - {member['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {member['email']}")
                    st.write(f"**Phone:** {member['phone']}")
                    st.write(f"**Membership Type:** {member['membershipType']}")
                with col2:
                    st.write(f"**Status:** {member['status']}")
                    st.write(f"**Join Date:** {member['joinDate']}")
                    st.write(f"**Last Interaction:** {member['lastInteraction']}")
                
                # Member Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View Documents", key=f"docs_{member['id']}"):
                        st.session_state.selected_member = member['id']
                        st.session_state.current_page = "Document Intelligence"
                with col2:
                    if st.button("View Interactions", key=f"inter_{member['id']}"):
                        st.session_state.selected_member = member['id']
                        st.session_state.current_page = "AI Insights"
                with col3:
                    if st.button("Edit Profile", key=f"edit_{member['id']}"):
                        st.session_state.selected_member = member['id']
                        st.session_state.edit_mode = True
    else:
        st.info("No members found matching the criteria.")

elif page == "Document Intelligence":
    st.title("📄 Document Intelligence")
    
    # Document Upload Section
    st.subheader("Upload New Document")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "png"])
    with col2:
        if uploaded_file:
            document_type = st.selectbox(
                "Document Type",
                options=["ID", "Contract", "Invoice", "Statement"]
            )
            if st.button("Upload"):
                st.success("Document uploaded successfully!")
    
    # Document List
    st.subheader("Document Library")
    documents = load_data("documents.json")
    if documents:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            doc_type_filter = st.multiselect(
                "Document Type",
                options=["ID", "Contract", "Invoice", "Statement"],
                default=["ID", "Contract", "Invoice", "Statement"]
            )
        with col2:
            status_filter = st.multiselect(
                "Status",
                options=["Verified", "Pending", "Rejected"],
                default=["Verified", "Pending", "Rejected"]
            )
        
        # Filter documents
        filtered_docs = [d for d in documents if d["documentType"] in doc_type_filter and d["status"] in status_filter]
        
        if filtered_docs:
            for doc in filtered_docs:
                with st.expander(f"{doc['documentType']} - {doc['status']}"):
                    st.write(f"**Upload Date:** {doc['uploadDate']}")
                    st.write(f"**Status:** {doc['status']}")
                    st.write(f"**URL:** {doc['url']}")
                    
                    # Document Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("View Details", key=f"view_{doc['id']}"):
                            st.session_state.selected_doc = doc['id']
                    with col2:
                        if st.button("Process Document", key=f"process_{doc['id']}"):
                            st.info("Document processing started...")
        else:
            st.info("No documents found matching the criteria.")
    else:
        st.info("No documents found. Run the data generation script first.")

elif page == "AI Insights":
    st.title("🤖 AI Insights")
    
    # Member selection
    members = load_data("members.json")
    if members:
        member_options = {f"{m['firstName']} {m['lastName']}": m["id"] for m in members}
        selected_member = st.selectbox("Select Member", options=list(member_options.keys()))
        
        if selected_member:
            member_id = member_options[selected_member]
            member = next(m for m in members if m["id"] == member_id)
            
            # Member Profile Card
            st.subheader("Member Profile")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="member-card">
                    <h3>{member['firstName']} {member['lastName']}</h3>
                    <p><strong>Email:</strong> {member['email']}</p>
                    <p><strong>Membership Type:</strong> {member['membershipType']}</p>
                    <p><strong>Status:</strong> {member['status']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="member-card">
                    <h3>Engagement Metrics</h3>
                    <p><strong>Join Date:</strong> {member['joinDate']}</p>
                    <p><strong>Last Interaction:</strong> {member['lastInteraction']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Interaction History
            st.subheader("Interaction History")
            interactions = load_data("interactions.json")
            member_interactions = [i for i in interactions if i["memberId"] == member_id]
            
            if member_interactions:
                # Interaction Timeline
                df = pd.DataFrame(member_interactions)
                df['date'] = pd.to_datetime(df['date'])
                
                fig = px.timeline(df, 
                                x_start="date", 
                                x_end="date",
                                y="type",
                                color="status",
                                title="Member Interaction Timeline")
                st.plotly_chart(fig, use_container_width=True)
                
                # Interaction Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Interactions", len(member_interactions))
                with col2:
                    completed = len([i for i in member_interactions if i["status"] == "Completed"])
                    st.metric("Completed", completed)
                with col3:
                    pending = len([i for i in member_interactions if i["status"] == "Pending"])
                    st.metric("Pending", pending)
                
                # Interaction Table
                st.dataframe(pd.DataFrame(member_interactions), use_container_width=True)
            else:
                st.info("No interactions found for this member.")
            
            # Document History
            st.subheader("Document History")
            documents = load_data("documents.json")
            member_documents = [d for d in documents if d["memberId"] == member_id]
            
            if member_documents:
                # Document Status Chart
                doc_df = pd.DataFrame(member_documents)
                fig = px.pie(doc_df, names='status', title='Document Status Distribution')
                st.plotly_chart(fig, use_container_width=True)
                
                # Document Table
                st.dataframe(pd.DataFrame(member_documents), use_container_width=True)
            else:
                st.info("No documents found for this member.")
            
            # AI Recommendations
            st.subheader("AI Recommendations")
            with st.expander("View Recommendations"):
                st.info("Based on member's interaction history and document status, here are some recommendations:")
                st.write("1. Schedule a follow-up call to discuss recent document submissions")
                st.write("2. Consider upgrading membership based on engagement level")
                st.write("3. Send a welcome package for new members")
    else:
        st.info("No members found. Run the data generation script first.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Member 360 Agentic AI v1.0") 