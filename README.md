# Running Instructions

## Developer Docs
Developer documentation can be found [here](https://spectrum-dev.notion.site/Developer-Documentation-0811ab7d0e5a4190ad9515929c8d90c5).

## Set up pre-commit hook for linting
1. `pip install pre-commit`
2. `pre-commit install`
Now, each time you make a commit, git cleans up the directory by linting your files first. You should then rerun your commit with the same message with the linted files.

## Running Tests
- `docker-compose up --build test`

## Running Check Lint
- `docker-compose up --build test-lint`

## Running Fix Lint
- `docker-compose up --build lint`

## Running Coverage
- `docker-compose up --build test-coverage`

## Running CLI and Specific Tests
- `docker-compose run --rm block-monolith /bin/bash`
- This will now boot up a shell of the block-monolith
- To run tests specifically on modules of code (for example, Signal Blocks ->  Test Saddle Block -> GetSaddleType), run `./manage.py test signal_blocks.tests.test_saddle_block.GetSaddleType`.
