#!/bin/bash

# Create GitHub milestones for the project
milestones=(
  "Set Up GitHub Action Workflow"
  "Configure Repository Secrets"
  "Modify Cline's Backend for API Integration"
  "Deploy the AI Agent Service"
  "Handle Different Change Formats"
  "Implement Security and Permissions"
  "Test the Implementation"
  "Iterate and Refine"
)

for title in "${milestones[@]}"; do
  gh api --method POST /repos/nimishchaudhari/cline_github_agent/milestones \
    -f title="$title" \
    -f state="open"
done
