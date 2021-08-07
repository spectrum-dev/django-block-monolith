# Running Instructions

## Developer Docs
Developer documentation can be found [here](https://spectrum-dev.notion.site/Developer-Documentation-0811ab7d0e5a4190ad9515929c8d90c5).


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
