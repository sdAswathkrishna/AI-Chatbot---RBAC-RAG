import streamlit as st
import requests
import json
from typing import Dict, Any, Optional
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="RAG-RBAC Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

class APIClient:
    """Client for communicating with the FastAPI backend"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def _get_auth_headers(self, username: str, password: str) -> Dict[str, str]:
        """Create basic auth headers"""
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"Authorization": f"Basic {credentials}"}
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.get(f"{self.base_url}/login", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Invalid credentials"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def chat(self, username: str, password: str, message: str) -> Dict[str, Any]:
        """Send chat message"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.post(
                f"{self.base_url}/chat",
                headers=headers,
                params={"message": message}
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_users(self, username: str, password: str) -> Dict[str, Any]:
        """Get all users (admin only)"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.get(f"{self.base_url}/admin/users", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def create_user(self, admin_username: str, admin_password: str, 
                   new_username: str, new_password: str, role: str) -> Dict[str, Any]:
        """Create new user (admin only)"""
        try:
            headers = self._get_auth_headers(admin_username, admin_password)
            headers["Content-Type"] = "application/json"
            payload = {
                "username": new_username,
                "password": new_password,
                "role": role
            }
            response = requests.post(
                f"{self.base_url}/admin/users",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def delete_user(self, admin_username: str, admin_password: str, username: str) -> Dict[str, Any]:
        """Delete user (admin only)"""
        try:
            headers = self._get_auth_headers(admin_username, admin_password)
            response = requests.delete(f"{self.base_url}/admin/users/{username}", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def init_vector_store(self, username: str, password: str) -> Dict[str, Any]:
        """Initialize vector store"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.post(f"{self.base_url}/admin/index/init", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def index_documents(self, username: str, password: str, batch_size: int = 50) -> Dict[str, Any]:
        """Index all documents"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.post(
                f"{self.base_url}/admin/index/documents",
                headers=headers,
                params={"batch_size": batch_size}
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_stats(self, username: str, password: str) -> Dict[str, Any]:
        """Get indexing statistics"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.get(f"{self.base_url}/admin/index/stats", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def clear_vector_store(self, username: str, password: str) -> Dict[str, Any]:
        """Clear vector store"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.delete(f"{self.base_url}/admin/index/clear", headers=headers)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def reindex_documents(self, username: str, password: str, batch_size: int = 50) -> Dict[str, Any]:
        """Reindex all documents"""
        try:
            headers = self._get_auth_headers(username, password)
            response = requests.post(
                f"{self.base_url}/admin/index/reindex",
                headers=headers,
                params={"batch_size": batch_size}
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Error: {response.status_code}"}
        except requests.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

# Initialize API client
api_client = APIClient(API_BASE_URL)

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "password" not in st.session_state:
        st.session_state.password = ""
    if "user_role" not in st.session_state:
        st.session_state.user_role = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "page" not in st.session_state:
        st.session_state.page = "login"

def login_page():
    """Render login page"""
    st.title("🤖 RAG-RBAC Chatbot")
    st.subheader("Please log in to continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if username and password:
                    with st.spinner("Authenticating..."):
                        result = api_client.login(username, password)
                    
                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.password = password
                        st.session_state.user_role = result["data"]["role"]
                        st.session_state.page = "chat"
                        st.success(f"Welcome {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.error("Please enter both username and password")

def chat_page():
    """Render chat interface"""
    st.title("💬 RAG Chatbot")
    
    # Sidebar with user info and navigation
    with st.sidebar:
        st.write(f"**Logged in as:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.user_role}")
        
        st.divider()
        
        # Navigation
        if st.button("🏠 Chat", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
        
        if st.session_state.user_role == "admin":
            if st.button("⚙️ Admin Dashboard", use_container_width=True):
                st.session_state.page = "admin"
                st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.password = ""
            st.session_state.user_role = ""
            st.session_state.chat_history = []
            st.session_state.page = "login"
            st.rerun()
        
        # Clear chat history
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat interface
    st.subheader(f"Hello {st.session_state.username}! Ask me anything.")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, (user_msg, bot_response) in enumerate(st.session_state.chat_history):
            # User message
            with st.chat_message("user"):
                st.write(user_msg)
            
            # Bot response
            with st.chat_message("assistant"):
                if isinstance(bot_response, dict) and "response" in bot_response:
                    st.write(bot_response["response"])
                    
                    # Show sources if available
                    if "sources" in bot_response and bot_response["sources"]:
                        with st.expander("📚 Sources"):
                            for j, source in enumerate(bot_response["sources"], 1):
                                st.write(f"**{j}. {source.get('title', 'Unknown')}**")
                                st.write(f"- Source: {source.get('source', 'Unknown')}")
                                st.write(f"- Role: {source.get('role', 'general')}")
                                st.write(f"- Relevance Score: {source.get('score', 0):.3f}")
                                if source.get('structured_data'):
                                    st.write(f"- Structured Data: {source['structured_data']}")
                                st.divider()
                    
                    # Show metadata
                    if "metadata" in bot_response:
                        with st.expander("ℹ️ Response Metadata"):
                            metadata = bot_response["metadata"]
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Total Sources", metadata.get("total_sources", 0))
                                st.metric("Avg Relevance", f"{metadata.get('average_relevance_score', 0):.3f}")
                            
                            with col2:
                                st.metric("Total Words", metadata.get("total_words_referenced", 0))
                                st.write(f"**Role Distribution:**")
                                for role, count in metadata.get("role_distribution", {}).items():
                                    st.write(f"- {role}: {count}")
                else:
                    st.write(bot_response)
    
    #     st.markdown("""
    # <style>
    # .stForm > div > div:nth-child(2) button {
    #     margin-top: 8px !important;
    # }
    # </style>
    # """, unsafe_allow_html=True)

    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input("Type your message here...", placeholder="Ask me anything!")
        
        with col2:
            st.write("")  # Add empty space
            st.write("")
            submit = st.form_submit_button("Send", use_container_width=True)
        
        if submit and user_input:
            # Add user message to history
            with st.spinner("Generating response..."):
                result = api_client.chat(st.session_state.username, st.session_state.password, user_input)
            
            if result["success"]:
                response = result["data"]
                
                # Check if response indicates no accessible documents
                if (isinstance(response, dict) and 
                    "response" in response and 
                    ("no relevant documents" in response["response"].lower() or 
                    "not provided in accessible documents" in response["response"].lower())):
                    
                    # Custom message for RBAC restrictions
                    rbac_message = f"Sorry, the information you're looking for is not available in documents accessible to your role ({st.session_state.user_role}). Please contact your administrator or try asking about topics related to your department."
                    st.session_state.chat_history.append((user_input, rbac_message))
                else:
                    st.session_state.chat_history.append((user_input, response))
            else:
                error_msg = f"Error: {result['error']}"
                st.session_state.chat_history.append((user_input, error_msg))
            
            st.rerun()

        # Alternative Solution 2: Using empty space above the button
        # Replace the above form with this version:

        # with st.form("chat_form", clear_on_submit=True):
        #     col1, col2 = st.columns([4, 1])
        #     
        #     with col1:
        #         user_input = st.text_input("Type your message here...", placeholder="Ask me anything!")
        #     
        #     with col2:
        #         st.write("")  # Add empty space
        #         submit = st.form_submit_button("Send", use_container_width=True)


def admin_dashboard():
    """Render admin dashboard"""
    st.title("⚙️ Admin Dashboard")
    
    # Sidebar navigation
    with st.sidebar:
        st.write(f"**Logged in as:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.user_role}")
        
        st.divider()
        
        if st.button("🏠 Chat", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
        
        if st.button("⚙️ Admin Dashboard", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.password = ""
            st.session_state.user_role = ""
            st.session_state.chat_history = []
            st.session_state.page = "login"
            st.rerun()
    
    # Check if user is admin
    if st.session_state.user_role != "admin":
        st.error("Access denied. Admin privileges required.")
        return
    
    # Tabs for different admin functions
    tab1, tab2, tab3 = st.tabs(["👥 User Management", "📚 Document Indexing", "📊 System Statistics"])
    
    with tab1:
        st.subheader("User Management")
        
        # Create new user
        st.write("### Create New User")
        with st.form("create_user_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_username = st.text_input("Username")
            with col2:
                new_password = st.text_input("Password", type="password")
            with col3:
                new_role = st.selectbox("Role", ["engineering", "marketing", "finance", "hr", "c-level", "admin", "general"])
            
            create_button = st.form_submit_button("Create User")
            
            if create_button:
                if new_username and new_password and new_role:
                    with st.spinner("Creating user..."):
                        result = api_client.create_user(
                            st.session_state.username, 
                            st.session_state.password,
                            new_username, 
                            new_password, 
                            new_role
                        )
                    
                    if result["success"]:
                        st.success(f"User '{new_username}' created successfully!")
                    else:
                        st.error(f"Failed to create user: {result['error']}")
                else:
                    st.error("Please fill in all fields")
        
        st.divider()
        
        # List and delete users
        st.write("### Current Users")
        if st.button("🔄 Refresh User List"):
            st.rerun()
        
        with st.spinner("Loading users..."):
            result = api_client.get_users(st.session_state.username, st.session_state.password)
        
        if result["success"]:
            users = result["data"]
            
            if users:
                for user in users:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**{user['username']}**")
                    with col2:
                        st.write(f"Role: {user['role']}")
                    with col3:
                        if user['username'] != st.session_state.username:  # Prevent self-deletion
                            if st.button(f"🗑️", key=f"delete_{user['username']}", help=f"Delete {user['username']}"):
                                with st.spinner(f"Deleting {user['username']}..."):
                                    delete_result = api_client.delete_user(
                                        st.session_state.username,
                                        st.session_state.password,
                                        user['username']
                                    )
                                
                                if delete_result["success"]:
                                    st.success(f"User '{user['username']}' deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete user: {delete_result['error']}")
            else:
                st.info("No users found")
        else:
            st.error(f"Failed to load users: {result['error']}")
    
    with tab2:
        st.subheader("Document Indexing Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Vector Store Operations")
            
            if st.button("🔧 Initialize Vector Store", use_container_width=True):
                with st.spinner("Initializing vector store..."):
                    result = api_client.init_vector_store(st.session_state.username, st.session_state.password)
                
                if result["success"]:
                    st.success("Vector store initialized successfully!")
                else:
                    st.error(f"Failed to initialize: {result['error']}")
            
            batch_size = st.number_input("Batch Size", min_value=10, max_value=200, value=50)
            
            if st.button("📚 Index All Documents", use_container_width=True):
                with st.spinner("Indexing documents... This may take a while."):
                    result = api_client.index_documents(
                        st.session_state.username, 
                        st.session_state.password, 
                        batch_size
                    )
                
                if result["success"]:
                    data = result["data"]
                    st.success(f"Indexing completed! Total chunks: {data.get('total_chunks', 0)}")
                else:
                    st.error(f"Failed to index documents: {result['error']}")
            
            if st.button("🔄 Reindex All Documents", use_container_width=True):
                with st.spinner("Reindexing documents... This may take a while."):
                    result = api_client.reindex_documents(
                        st.session_state.username, 
                        st.session_state.password, 
                        batch_size
                    )
                
                if result["success"]:
                    data = result["data"]
                    st.success(f"Reindexing completed! Total chunks: {data.get('total_chunks', 0)}")
                else:
                    st.error(f"Failed to reindex documents: {result['error']}")
        
        with col2:
            st.write("### ⚠️ Danger Zone")
            
            st.error("**Warning: This action will delete all indexed data!**")
            
            confirm_clear = st.checkbox("I understand this will delete all data")
            
            if st.button("🗑️ Clear Vector Store", 
                        use_container_width=True, 
                        disabled=not confirm_clear,
                        type="primary"):
                
                with st.spinner("Clearing vector store..."):
                    result = api_client.clear_vector_store(st.session_state.username, st.session_state.password)
                
                if result["success"]:
                    st.success("Vector store cleared successfully!")
                else:
                    st.error(f"Failed to clear vector store: {result['error']}")
    
    with tab3:
        st.subheader("System Statistics")
        
        if st.button("🔄 Refresh Stats"):
            st.rerun()
        
        with st.spinner("Loading statistics..."):
            result = api_client.get_stats(st.session_state.username, st.session_state.password)
        
        if result["success"]:
            stats = result["data"]
            
            # Main metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Data Points", stats.get("total_points", 0))
            with col2:
                st.metric("Vector Size", stats.get("vector_size", 0))
            with col3:
                st.metric("Avg Words/Chunk", f"{stats.get('avg_words_per_chunk', 0):.1f}")
            with col4:
                st.metric("Sample Size", stats.get("sample_size", 0))
            
            # Role distribution
            st.write("### Role Distribution")
            role_dist = stats.get("role_distribution", {})
            if role_dist:
                for role, count in role_dist.items():
                    st.write(f"**{role.title()}:** {count} documents")
            else:
                st.info("No role distribution data available")
            
            # File type distribution
            st.write("### File Type Distribution")
            file_type_dist = stats.get("file_type_distribution", {})
            if file_type_dist:
                for file_type, count in file_type_dist.items():
                    st.write(f"**{file_type.upper()}:** {count} files")
            else:
                st.info("No file type distribution data available")
            
            # Additional info
            st.write("### System Info")
            st.write(f"**Collection Name:** {stats.get('collection_name', 'Unknown')}")
            st.write(f"**Distance Metric:** {stats.get('distance', 'Unknown')}")
            
        else:
            st.error(f"Failed to load statistics: {result['error']}")

def main():
    """Main application logic"""
    init_session_state()
    
    # Check if backend is accessible
    try:
        response = requests.get(f"{API_BASE_URL}/login", timeout=5)
    except requests.RequestException:
        st.error("🚨 Cannot connect to backend server. Please ensure the FastAPI server is running on http://localhost:8000")
        st.stop()
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.page == "chat":
            chat_page()
        elif st.session_state.page == "admin":
            admin_dashboard()
        else:
            chat_page()

if __name__ == "__main__":
    main()