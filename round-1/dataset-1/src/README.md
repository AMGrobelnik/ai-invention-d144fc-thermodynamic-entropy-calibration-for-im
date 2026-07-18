# Text Classification Datasets for LLM Calibration Evaluation

## Overview
This dataset collection contains 5 standardized text classification datasets suitable for evaluating LLM confidence calibration methods. All datasets have been downloaded from HuggingFace Hub, standardized to a unified JSON schema, and split into train/validation/test sets.

## Datasets

### 1. SST-2 (Stanford Sentiment Treebank)
- **Task**: Binary sentiment classification
- **Classes**: 2 (negative, positive)
- **Expected Difficulty**: Easy (high LLM accuracy >80%)
- **Splits**: train=10,000, validation=872, test=1,821
- **Source**: GLUE benchmark, Stanford NLP

### 2. AG News
- **Task**: Topic classification
- **Classes**: 4 (World, Sports, Business, Sci/Tech)
- **Expected Difficulty**: Easy to moderate
- **Splits**: train=20,000, validation=5,000, test=7,600
- **Source**: AG's News Corpus

### 3. MNLI (Multi-Genre NLI)
- **Task**: Natural Language Inference
- **Classes**: 3 (entailment, neutral, contradiction)
- **Expected Difficulty**: Moderate
- **Splits**: train=50,000, validation=9,815, test=9,832
- **Source**: GLUE benchmark

### 4. QNLI (Question NLI)
- **Task**: Question-answering NLI
- **Classes**: 2 (entailment, not_entailment)
- **Expected Difficulty**: Moderate to challenging
- **Splits**: train=20,000, validation=2,731, test=2,732
- **Source**: GLUE benchmark

### 5. DBpedia
- **Task**: Ontology classification
- **Classes**: 14 (various ontology classes)
- **Expected Difficulty**: Moderate
- **Splits**: train=50,000, validation=10,000, test=70,000
- **Source**: DBpedia extraction

## File Structure

```
temp/datasets/
├── dataset_summary.json          # Complete summary with statistics
├── sst-2_train.json            # Full training set
├── sst-2_validation.json       # Validation set (for temperature tuning)
├── sst-2_test.json             # Test set
├── mini_sst-2_train.json      # Mini version (100 rows)
├── preview_sst-2_train.json    # Preview version (3 rows)
├── ... (similar for all datasets)
```

## JSON Schema

All dataset files follow this unified schema:

```json
{
  "text": "<input text string>",
  "label": <integer label, 0-indexed>,
  "label_text": "<optional human-readable label>",
  "metadata": {
    "dataset_name": "<source dataset>",
    "split": "<train|validation|test>",
    "original_label": "<original label format>"
  }
}
```

## Usage

1. **Training**: Use `*_train.json` files
2. **Temperature Tuning**: Use `*_validation.json` files (1-5K examples, sufficient for tuning)
3. **Evaluation**: Use `*_test.json` files
4. **Development/Testing**: Use `mini_*.json` files (100 rows)
5. **Inspection**: Use `preview_*.json` files (3 rows)

## Total Size
- All full datasets combined: **116MB** (under 300MB limit)
- Mini variants: ~2MB total
- Preview variants: <100KB total

## Reproducibility

The following scripts were used to create this dataset collection:
1. `preview_datasets.py` - Initial dataset preview and inspection
2. `download_and_standardize.py` - Download and standardize datasets
3. `subsample_datasets.py` - Reduce dataset sizes to meet size constraints

## Validation

All datasets have been validated for:
- ✅ Correct JSON schema (all required fields present)
- ✅ Integer labels (0-indexed)
- ✅ Non-empty text fields
- ✅ Proper train/validation/test splits
- ✅ Stratified sampling (preserves class distribution)

## Benchmark Provenance

All datasets are established benchmarks:
- SST-2, MNLI, QNLI: Part of GLUE benchmark (Wang et al., 2018)
- AG News: Established topic classification benchmark
- DBpedia: Standard ontology classification dataset

## Next Steps

These datasets are ready for:
1. LLM prompt-based classification experiments
2. Confidence calibration method evaluation
3. Temperature scaling and model calibration research
