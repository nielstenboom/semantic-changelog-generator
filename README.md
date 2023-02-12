# Semantic changelog generator

This action prints generates a pretty changelog from semantic commits

## Inputs

## `base`

**Required** The base ref for git log

## `head`

**Required** The head ref for git log

## Outputs

## `changelog`

The generated changelog

## Example usage

```yaml
- uses: nielstenboom/semantic-changelog-generator@main
  id: changelog
  with:
    base: main
    head: v1.0.0

- name: Get the changelog
  run: |
    cat << "EOF"
    ${{ steps.changelog.outputs.changelog }}
    EOF
```
