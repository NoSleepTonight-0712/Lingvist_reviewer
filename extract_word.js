wd_list = document.getElementsByClassName('wordlist-item');

result_string = "";

field_splitter = "=*#&^!="
word_splitter = "$%d82@$="

var word, sentence, metaPoints, lastAnswered, practiced;

for (let i = 0; i < wd_list.length; i++) {
    wd = wd_list[i];

    // word
    word = wd.querySelector('.homograph .target')?.textContent.trim().replace('\n', " ").replace('                     ', ' ')

    // sentence
    sentence = wd.querySelector('.context.target')?.textContent.trim();

    // last practice
    metaPoints = wd.querySelectorAll('.meta .data-point');
    lastAnswered = metaPoints[0]?.textContent.trim();
    practiced = metaPoints[1]?.textContent.trim();

    result_string_element = `${word}${field_splitter}${sentence}${field_splitter}${lastAnswered}${field_splitter}${practiced}`;

    if (i != wd_list.length - 1) {
        result_string_element += word_splitter;
    }
    result_string = result_string + result_string_element;
}

console.log(result_string);


