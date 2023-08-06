A very-simple-subset-of-haskell fuzzer

```
module Generated (function0,function1,function2) where

function0 :: Int -> Bool -> Bool -> Bool -> Bool -> Int -> Int
function0 a b c d e f = (function1 (2 /= 7) False False)

function1 :: Bool -> Bool -> Bool -> Int
function1 a b c = (8 * 0)

function2 :: Bool -> Int
function2 a = 1
```

it's available on pip by `pip install huzzer`

## Setup
Make sure you have python3 on your machine (`which python3` should print a path to it).

Set up a `virtualenv` with `virtualenv -p \`which python3\` env`

Activate the environment with `source env/bin/activate`

Install requirements `pip install -r requirements.txt`

Then you should be good to go. To leave the virtualenv, type `deactivate`

## Testing
To run all of the tests, run `nosetests`.

To run larger acceptance tests (against the ghc compiler), you will need `ghc` and `parallel` installed.
run `./large_acceptance_test.sh <number of tests>`

## TODOs
* multiple definitions for functions
* some unary expressions (fromEnum, !, abs)
* more commandline arguments for customisation


