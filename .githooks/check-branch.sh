#!/bin/bash

CURRENT_BRANCH=$(git branch --show-current)

PROTECTED_BRANCHES=("main" "master")

for branch in "${PROTECTED_BRANCHES[@]}"; do
    if [ "$CURRENT_BRANCH" = "$branch" ]; then
        echo "🚫 ERROR: Direct commits to '$branch' branch are not allowed!"
        echo "💡 Please create a feature branch:"
        echo "   git checkout -b feature/your-feature-name"
        echo "   make your changes and commit"
        echo "   git push origin feature/your-feature-name"
        echo "   Create a Pull Request"
        exit 1
    fi
done

echo "✅ Committing to branch: $CURRENT_BRANCH"
exit 0
