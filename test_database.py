import json
from io_database import run_db


def run_test(commands):
    commands = commands + ['END']
    inputs = iter(commands)

    def mock_input(prompt=''):
        return next(inputs)

    original_input = __builtins__.input
    __builtins__.input = mock_input
    outputs = []

    def mock_print(*output):
        outputs.append(' '.join(str(a) for a in output))

    original_print = __builtins__.print
    __builtins__.print = mock_print
    run_db()
    __builtins__.input = original_input
    __builtins__.print = original_print
    return outputs


def load_tests():
    with open('tests.json') as f:
        return json.load(f)


if __name__ == '__main__':
    for test in load_tests():
        print(f'\n🔹 Тест: {test["name"]}')
        actual = run_test(test['commands'])

        if actual == test['expected']:
            print('✅ Успех')
        else:
            print('❌ Ошибка')
            print('Ожидалось: ', test['expected'])
            print('Получено: ', actual)
