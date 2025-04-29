from collections import defaultdict, deque


class Transaction:
    def __init__(self):
        self.updates = {}
        self.deletes = set()


class Database:
    def __init__(self):
        self.data = {}
        self.value_counts = defaultdict(int)
        self.transaction_deque = deque()

    def set(self, key, value):
        transaction = self._get_current_transaction()
        if transaction is None:
            self._set_impl(key, value)
        else:
            # Удаляем из списка удалений, если был UNSET
            if key in transaction.deletes:
                transaction.deletes.remove(key)
            transaction.updates[key] = value

    def get(self, key):
        # Проверяем транзакции от самой новой к старой
        for transaction in reversed(self.transaction_deque):
            if key in transaction.deletes:
                return 'NULL'
            if key in transaction.updates:
                return transaction.updates[key]
        return self.data.get(key, 'NULL')

    def unset(self, key):
        transaction = self._get_current_transaction()
        if transaction is None:
            self._unset_impl(key)
        else:
            # Добавляем в список удалений
            if key in transaction.updates:
                del transaction.updates[key]
            transaction.deletes.add(key)

    def counts(self, value):
        visible = self._get_all_visible_items()
        return sum(1 for v in visible.values() if v == value)

    def find(self, value):
        visible = self._get_all_visible_items()
        result = [k for k, v in visible.items() if v == value]
        return ' '.join(sorted(result)) if result else 'NULL'

    def begin(self):
        self.transaction_deque.append(Transaction())

    def rollback(self):
        if not self.transaction_deque:
            return 'NO TRANSACTION'
        self.transaction_deque.pop()
        return

    def commit(self):
        if not self.transaction_deque:
            return 'NO TRANSACTION'
        # Применяем изменения от самой старой транзакции к самой новой
        while self.transaction_deque:
            transaction = self.transaction_deque.popleft()
            for key in transaction.deletes:
                self._unset_impl(key)
            for key, value in transaction.updates.items():
                self._set_impl(key, value)
        return

    def _decrement_counter(self, value):
        self.value_counts[value] -= 1
        if self.value_counts[value] == 0:
            del self.value_counts[value]

    def _set_impl(self, key, value):
        # Обновляем счетчики для старого значения.
        old_value = self.data.get(key)
        if old_value:
            self._decrement_counter(old_value)
        self.data[key] = value
        # Обновляем счетчики для нового значения
        self.value_counts[value] += 1

    def _unset_impl(self, key):
        if key in self.data:
            self._decrement_counter(self.data[key])
            del self.data[key]

    def _get_current_transaction(self):
        return self.transaction_deque[-1] if self.transaction_deque else None

    def _get_all_visible_items(self):
        visible = dict(self.data)
        for transaction in self.transaction_deque:
            for key in transaction.deletes:
                visible.pop(key)
            visible.update(transaction.updates)
        return visible


def run_db():
    db = Database()

    while True:
        try:
            line = input('> ').rstrip()
        except EOFError:
            break

        if not line:
            continue

        command_parts = line.split()
        command = command_parts[0].upper()

        if command == 'END':
            break

        elif command == 'SET' and len(command_parts) == 3:
            db.set(command_parts[1], command_parts[2])

        elif command == 'GET' and len(command_parts) == 2:
            print(db.get(command_parts[1]))

        elif command == 'UNSET' and len(command_parts) == 2:
            db.unset(command_parts[1])

        elif command == 'COUNTS' and len(command_parts) == 2:
            print(db.counts(command_parts[1]))

        elif command == 'FIND' and len(command_parts) == 2:
            print(db.find(command_parts[1]))

        elif command == 'BEGIN':
            db.begin()

        elif command == 'ROLLBACK':
            error = db.rollback()
            if error:
                print(error)

        elif command == 'COMMIT':
            error = db.commit()
            if error:
                print(error)

        else:
            print('Unknown command')


if __name__ == '__main__':
    run_db()
