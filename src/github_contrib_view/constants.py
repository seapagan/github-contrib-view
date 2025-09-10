"""Define any required constants for this app."""

# define the GraphQL query string
QUERY = """
    query($username: String!) {
        user(login: $username) {
            contributionsCollection {
                contributionCalendar {
                    weeks {
                        contributionDays {
                            date
                            contributionCount
                        }
                    }
                }
            }
        }
    }
    """

HTTP_OK = 200
REQUEST_TIMEOUT = 10

# yeah this is (hopefully!) not going to change, but it makes the code more
# readable to have it as a constant.
DAYS_PER_WEEK = 7
