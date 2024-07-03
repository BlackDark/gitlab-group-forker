import gitlab
import argparse
import sys

import gitlab.v4
import gitlab.v4.objects


def fork_project(
    gl: gitlab.Gitlab,
    project: gitlab.v4.objects.Project,
    dest_group: gitlab.v4.objects.Group,
) -> None:
    try:
        # Fetch the full project object
        full_project = gl.projects.get(project.id)
        project_expected_path = f"{dest_group.full_path}/{full_project.path}"

        # Check if the project is archived or marked for deletion
        if (
            full_project.archived
            or full_project.marked_for_deletion_at is not None
            or full_project.marked_for_deletion_on is not None
        ):
            print(
                f"Skipping project {full_project.path_with_namespace} (archived or marked for deletion)"
            )
            return

        try:
            gl.projects.get(project_expected_path)

            print(f"Skipping project {project_expected_path} (already exists).")
            return
        except Exception:
            pass

        fork = full_project.forks.create(
            {
                "namespace_id": dest_group.id,
                "visibility": full_project.visibility,
                "avatar_url": full_project.avatar_url,
                "description": full_project.description,
            }
        )
        print(
            f"Forked project {full_project.path_with_namespace} to {fork.path_with_namespace}"
        )
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"Error forking project {project.path_with_namespace}: {e}")


def fork_group(
    gl: gitlab.Gitlab,
    src_group: gitlab.v4.objects.Group,
    dest_group: gitlab.v4.objects.Group,
) -> None:
    # Fork all projects in the current group
    projects = src_group.projects.list(all=True, archived=False)
    for project in projects:
        fork_project(gl, project, dest_group)

    # Recursively fork subgroups
    subgroups = src_group.subgroups.list(all=True)
    for subgroup in subgroups:
        # Fetch the full project object
        full_subgroup = gl.groups.get(subgroup.id)

        # Check if the subgroup is marked for deletion
        if full_subgroup.marked_for_deletion_on is not None:
            print(
                f"Skipping subgroup {full_subgroup.path_with_namespace} (marked for deletion)"
            )
            return

        subgroup_expected_path = f"{dest_group.full_path}/{full_subgroup.path}"
        create_subgroup = True
        new_dest_group: gitlab.v4.objects.Group = None

        try:
            new_dest_group = gl.groups.get(subgroup_expected_path)

            print(
                f"Skipping creation of subgroup {subgroup_expected_path} (already exists)."
            )
            create_subgroup = False
        except Exception:
            pass

        if create_subgroup:
            new_dest_group = gl.groups.create(
                {
                    "name": subgroup.name,
                    "path": subgroup.path,
                    "parent_id": dest_group.id,
                    "visibility": full_subgroup.visibility,
                    "avatar_url": full_subgroup.avatar_url,
                    "description": full_subgroup.description,
                }
            )
            print(f"Created subgroup {new_dest_group.full_path}")
        fork_group(gl, gl.groups.get(subgroup.id), new_dest_group)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fork GitLab groups recursively")
    parser.add_argument("--token", required=True, help="GitLab personal access token")
    parser.add_argument("--url", required=True, help="GitLab instance URL")
    parser.add_argument("--src-grp", required=True, help="Source group path or ID")
    parser.add_argument(
        "--dest-grp", required=True, help="Destination group path or ID"
    )
    args = parser.parse_args()

    gl = gitlab.Gitlab(args.url, private_token=args.token)

    try:
        src_group = gl.groups.get(args.src_grp)
    except gitlab.exceptions.GitlabGetError:
        print(f"Error: Source group '{args.src_grp}' not found")
        sys.exit(1)

    try:
        dest_group = gl.groups.get(args.dest_grp)
    except gitlab.exceptions.GitlabGetError:
        print(f"Error: Destination group '{args.dest_grp}' not found")
        sys.exit(1)

    fork_group(gl, src_group, dest_group)


if __name__ == "__main__":
    main()
