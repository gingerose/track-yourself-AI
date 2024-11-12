from models.base_collection_item import BaseCollectionItem


class BaseCollectionItemRepository:
    def __init__(self, db):
        self.db = db

    def add_item(self, collection_id, user_id, item_id, status, description):
        item = BaseCollectionItem(
            collection_id=collection_id,
            user_id=user_id,
            item_id=item_id,
            status=status,
            description=description
        )
        self.db.session.add(item)
        self.db.session.commit()
        return item

    def delete_item(self, id):
        item = BaseCollectionItem.query.get(id)
        if item:
            self.db.session.delete(item)
            self.db.session.commit()
            return True
        return False

    def get_items_by_user_and_collection(self, collection_id, user_id):
        items = BaseCollectionItem.query.filter_by(collection_id=collection_id, user_id=user_id).all()
        return items

    def get_items_count_by_status(self, collection_id, user_id):
        # Общее количество айтемов
        total_count = BaseCollectionItem.query.filter_by(collection_id=collection_id, user_id=user_id).count()

        # Количество айтемов со статусом 'DONE'
        done_count = BaseCollectionItem.query.filter_by(collection_id=collection_id, user_id=user_id,
                                                        status='DONE').count()

        return total_count, done_count

    def update_item_status(self, item_id, status):
        item = BaseCollectionItem.query.filter_by(id=item_id).first()
        if not item:
            return None

        item.status = status
        self.db.session.commit()
        return item
