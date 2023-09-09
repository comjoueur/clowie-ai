from models.entity import EntityModel
from models.entity_entry import EntityEntryModel
from models.source import SourceModel


def delete_all_indices_docs():
  EntityModel.delete_all()
  EntityEntryModel.delete_all()
  SourceModel.delete_all()
  return "All indices and docs deleted"
