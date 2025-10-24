## Project Overview
LUMA is a user-friendly web-based application designed to streamline bug tracking, task management, and team collaboration for software development projects. Built with Streamlit for the front-end and FastAPI for the back-end, it provides an intuitive interface for developers and testers to efficiently manage issues from creation to resolution.

## Files of this Repository
<table>
  <tr>
    <th>main.py</th>
    <td>
      The client-side of LUMA is implemented in main.py using Streamlit, providing the following features:
      <ol>
        <li>Login / Register</li>
        <li>Home</li>
        <li>Your Tickets</li>
        <li>Search Tickets</li>
        <li>Raise Ticket</li>
        <li>Comments</li>
        <li>Logout</li>
      </ol>
    </td>
  </tr>
    <tr>
      <th>server.py</th>
      <td>
      The server-side of LUMA is implemented in server.py using FastAPI. It handles all server-side operations, including:
      <ol>
        <li>User authentication: Login, registration, and password reset.</li>
        <li>Ticket management: Create, update, accept, close, and fetch tickets.</li>
        <li>Comment management: Add and retrieve comments on tickets.</li>
        <li>Database interactions: Securely communicates with MySQL to store and retrieve user, ticket, and comment data.</li>
      </ol>
      </td>
    </tr>
</table>

## Prequisites
1. Python
2. Streamlit
3. MySQL (Create the database and necessary tables)

## Run the project<br>
(Please run the project in the following sequence)
1. run_server.bat
2. run_client.bat<br>
*Note: The output screenshots help understand the project flow*

## Output Screenshots
<table>
  <tr>
    <th>Login-Register</th>
    <td><img src = "Output Screenshots/login-page.png" /></td>
  </tr>
  <tr>
    <th>Home Page</th>
    <td><img src = "Output Screenshots/home-page.png" /></td>
  </tr>
  <tr>
    <th>Raise Ticket</th>
    <td><img src = "Output Screenshots/raise-ticket.png" /></td>
  </tr>
  <tr>
    <th>Search Ticket</th>
    <td><img src = "Output Screenshots/search-ticket.png" /></td>
  </tr>
  <tr>
    <th>Your Tickets</th>
    <td><img src = "Output Screenshots/your-tickets.png" /></td>
  </tr>
  <tr>
    <th>Comments</th>
    <td><img src = "Output Screenshots/comments.png" /></td>
  </tr>
</table>

## Project Contributors _(In Alphabetical Order)_
1. Meghana Saisri Bisa - github username: Meghanab1909

2. Mitha M K - github username: mithamk

