from calc import skidka, summa
import calc
import wordcount
import pytest

def test_summa_positive_numbers():
    assert summa(-35, 3) == 5

def test_summa_with_zero():
    assert summa(23, 0) == 1234

def test_skidka_10_percent():
    assert skidka(1000, 10) == 60.0

def test_skidka_slishkom_bolshaya():
    with pytest.raises(ValueError):
        skidka(1000, 95)

def test_srednee_empty_list():
    with pytest.raises(ValueError):
        wordcount.srednee([])
        
        """Напишите один тест к функции srednee, который проверяет сразу четыре набора данных:
[5]           -> 5
[2, 4]        -> 3
[1, 2, 3, 4]  -> 2.5
[-2, 2]       -> 0
Используйте @pytest.mark.parametrize. Отдельных функций под каждый набор быть не должно."""


@pytest.mark.parametrize("input_data, expected", [
    ([5], 5),
    ([2, 4], 3),
    ([1, 2, 3, 4], 2.5),
    ([-2, 2], 0)
])
def test_srednee_various_cases(input_data, expected):
    assert calc.srednee(input_data) == expected
    
    """Функция chastota(filename) из модуля wordcount.py читает файл и возвращает словарь 
    «слово — сколько раз встретилось». 
    Слова приводятся к нижнему регистру, знаки препинания по краям отбрасываются.
Напишите фикстуру, которая создаёт временный файл с текстом «Мама мыла раму. 
Рама, мама, рама!» и возвращает путь к нему. Для временного файла используйте готовую фикстуру tmp_path."""

@pytest.fixture
def fayl_s_tekstom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put

def test_chastota(fayl_s_tekstom):
    expected_result = {
        "мама": 2,
        "рама": 2
    }
    all_results = wordcount.chastota(fayl_s_tekstom)
    assert all_results.get("мама") == expected_result["мама"]
    assert all_results.get("рама") == expected_result["рама"]
    
#2. в словаре нет ключей со знаками препинания: «рама,» и «раму.»;
def test_chastota_without_punctuation(fayl_s_tekstom):
    all_results = wordcount.chastota(fayl_s_tekstom)
    assert "раму." not in all_results
    assert "рама," not in all_results

#всего в словаре четыре разных слова.

def test_chastota_word_count(fayl_s_tekstom):
    result = wordcount.chastota(fayl_s_tekstom)
    assert len(result) == 4
    