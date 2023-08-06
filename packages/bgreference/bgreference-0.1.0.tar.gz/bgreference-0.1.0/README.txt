# BGREFERENCE #

bgreference is a library to fast retrive Genome Reference partial sequences.

## Installation using pip
```
pip install bgreference
```

## Installation using conda
```
conda install -c bbglab bgreference
```

## Usage example HG19

```
#!python
from bgreference import hg19, hg38

# Get 10 bases from chromosome one build hg19
tenbases = hg19('1', 12345, size=10)

# Get 10 bases from chromosome one builg hg38

```