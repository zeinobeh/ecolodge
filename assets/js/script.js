
var message_tag = document.getElementById("message_box");
function buttonclose(){ 
   message_tag.style.display = "none"; 
}; 


// مربوط به انتخاب شهر براساس استان

const provinceSelect = document.getElementById("province");
const citySelect = document.getElementById("city");

if (provinceSelect && citySelect) {

    const cities = {
        "اردبیل": ["اردبیل", "سرعین"],
        "اصفهان": ["کاشان", "اصفهان", ""],
        "خراسان رضوی": ["مشهد", "طرقبه", "شاندیز"],
        "فارس": ["شیراز", "", ""],
        "گیلان": ["رشت", "لاهیجان", "ماسال"],
        "گلستان": ["گرگان", "", ""],
        "مازندران": ["کلاردشت", "رامسر", "نوشهر", "چالوس"],
    };

    let province = provinceSelect.value;

    function showCities() {
        
        citySelect.innerHTML = '<option value="">همه شهرها</option>';

        province = provinceSelect.value;

    if (province in cities) {

        for (let city of cities[province]) {

            if (city == "{{ request.GET.city }}") {
                citySelect.innerHTML +=
                    '<option value="' + city + '" selected>' + city + '</option>';
            }
            else {
                citySelect.innerHTML +=
                    '<option value="' + city + '">' + city + '</option>';
            }

        }
    }
}

    // وقتی استان انتخاب میشود
    provinceSelect.addEventListener("change", function () {
        showCities();
    });

    // وقتی صفحه بعد از جستجو دوباره لود می‌شود
    showCities();
}
