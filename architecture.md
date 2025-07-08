# Git Workflow for Elastic Agent Configuration

This document outlines the architecture of the GitHub Actions workflow designed to automate the process of updating Elastic Agent configuration files.

## Plan for the Git Workflow

1.  **Workflow Trigger**: The workflow is triggered only on pull requests targeting the main branch that contain changes to `.yml` files located in subdirectories within the `inputs/` directory (e.g., `inputs/loc1/google_http/http_google.yml`). This excludes the `elastic-agent.yml` files located directly within `inputs/loc1/` or `inputs/loc2/`. The workflow will not trigger on direct commits to the main branch.
2.  **Identify Changed Files**: The workflow identifies all `.yml` files added or modified in the pull request.
3.  **Process Each Change**: For each changed input file, the workflow:
    *   **Validate Input File**: It first validates the YAML syntax of the changed input file. If invalid, the workflow will fail and report an error.
    *   **Determine Location**: It will find the parent directory (e.g., `loc1`, `loc2`).
    *   **Verify Main File**: It will check if `elastic-agent.yml` exists in that location. If not, it will fail.
    *   **Append Content**: The content of the valid input file will be appended to the `inputs:` section of the corresponding `elastic-agent.yml`.
4.  **Validate Main YAML**: After updating, the workflow will validate the `elastic-agent.yml` file's syntax.
5.  **Commit Changes**: If validation passes, the changes will be committed to the pull request branch.
6.  **Post PR Comment**: The workflow will post a comment on the pull request.
    *   On **success**, it will confirm that the files were updated.
    *   On **failure**, it will provide details about the error (e.g., invalid YAML, missing main file).

## Workflow Visualization

Here is a Mermaid diagram illustrating the planned workflow:

```mermaid
graph TD
    A[Start: Pull Request on 'inputs/**'] --> B{Get Changed Files};
    B --> C{For each changed file};
    C --> C1{Validate Input File YAML};
    C1 -- Invalid --> F[Fail Workflow];
    C1 -- Valid --> D{Get Location};
    D --> E{elastic-agent.yml exists?};
    E -- No --> F;
    E -- Yes --> G{Read Input File};
    G --> H{Read elastic-agent.yml};
    H --> I{Append Input to elastic-agent.yml};
    I --> J{Validate Main YAML};
    J -- Invalid --> F;
    J -- Valid --> K{Commit & Push Changes};
    K --> M{Post Success Comment on PR};
    M --> L[End];
    F --> N{Post Failure Comment on PR};
    N --> L;