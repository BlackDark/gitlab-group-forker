# GitLab Group Forker

GitLab Group Forker is a Python script that allows you to recursively fork GitLab groups, including all repositories and subgroups. It provides an easy way to duplicate entire group structures while ignoring archived and deleted projects.

## Features

- Recursively fork GitLab groups and their subgroups
- Fork all projects within the groups
- Ignore archived and deleted projects
- Support for forking into subgroups of existing groups

## Requirements

- Python 3.7+
- GitLab API access token with appropriate permissions

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/gitlab-group-forker.git
cd gitlab-group-forker
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:

```ps1
venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python fork_gitlab_group.py --token YOUR_GITLAB_TOKEN --url YOUR_GITLAB_URL --src-grp SOURCE_GROUP --dest-grp DESTINATION_GROUP
```

Replace the placeholders with your actual values:

- `YOUR_GITLAB_TOKEN`: Your GitLab personal access token
- `YOUR_GITLAB_URL`: The URL of your GitLab instance (e.g., https://gitlab.com)
- `SOURCE_GROUP`: The path or ID of the group you want to fork
- `DESTINATION_GROUP`: The path or ID of the group where you want to create the fork

Example:

```bash
python fork_gitlab_group.py --token abc123 --url https://gitlab.com --src-grp my-org/source-group --dest-grp my-org/destination-group
```

To fork into a subgroup of an existing group, specify the full path of the destination group:

```bash
python fork_gitlab_group.py --token abc123 --url https://gitlab.com --src-grp my-org/source-group --dest-grp my-org/parent-group/new-subgroup
```

## Notes

- Ensure that your GitLab token has the necessary permissions to read from the source group and create projects/groups in the destination group.
- The script will skip archived and deleted projects during the forking process.
- Forking large groups with many projects and subgroups may take a considerable amount of time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
