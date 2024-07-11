# Arcade Session Viewer

Arcade Session Viewer is a web application that allows users to view and manage their Hack Club Arcade sessions. It provides an easy-to-use interface for viewing the status of your sessions.

## Features

- View sessions grouped by goals and sorted by creation time
- Display session details including title, creation time, and duration
- Get Slack thread URLs for each session
- Check the review status of sessions
- User authentication using Slack user ID and Arcade API key

## Live Demo

You can access the live version of this application at: [https://arcade-session-viewer.artem4852.hackclub.app/](https://arcade-session-viewer.artem4852.hackclub.app/). See the [Usage](#usage) section for more information on how to use the application.

## Tech Stack

- Backend: Python with Flask
- Frontend: HTML, SASS, JavaScript
- API Integration: Slack API, Hack Hour API

## Local Setup and Installation

1. Clone the repository
2. Install the required Python packages:
   ```
   pip install flask requests python-dotenv
   ```
3. Set up your environment variables in a `.env` file (see how to get those [here](#slack-api-credentials)):
   ```
   cookie=your_slack_cookie
   token=your_slack_token
   ```
4. Run the application:
   ```
   python app.py
   ```

## Slack API credentials

To get your Slack API credentials, follow these steps:

1. Open Slack in your web browser
2. Open the developer console (F12)
3. Go to the "Network" tab
4. Reload the page
5. Click on any XHR request
6. Find the "cookie" in the "Request Headers" section and "token" in the "Request Payload" section

## Usage

1. Open the application in your web browser
2. Enter your [Slack user ID and Arcade API](#where-to-find-your-slack-user-id-and-arcade-api-key) key and click "Update credentials"
3. View your sessions grouped by goals
4. Click on "Load" to fetch Slack thread URLs and session statuses

If you click on "Load" for session status, thread URL will be loaded as well if it hasn't been yet.

### Where to find your Slack user ID and Arcade API key?

1. To get your user id go to channel #what-is-my-slack-id in the Hack Club Slack and type anything you wish. A bot will respond with your user id.
2. To get your Arcade API key use the command /api.

### Why did I not implement loading URLs and sessions' statuses when loading the page?

The thing is every such request requires a separate API call. Many users have a lot of sessions, and loading all of them at once would be inefficient and might even cause rate-limits and bans. That's why I decided to implement a button that would load the URLs and statuses only when the user needs them.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
