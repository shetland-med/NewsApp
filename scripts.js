document.addEventListener('DOMContentLoaded', function () {
    var newsDataElement = document.getElementById('news-data');
    var newsData = JSON.parse(newsDataElement.textContent);
    var appsDataElement = document.getElementById('app-data');
    var appsData = JSON.parse(appsDataElement.textContent);
    var previous_newsDataElement = document.getElementById('previous-data');
    var previous_newsData = JSON.parse(previous_newsDataElement.textContent);


    new Vue({
        el: '#app',
        delimiters: ['${', '}'],//Vue.jsのデリミタを変更
        data: {
            newsData: newsData,
            appsData: appsData,
            previous_newsData: previous_newsData,
            selectedNews: [],
            selectedApps: [],
            showModal: false,
            displayApps: "",
            categories: [],
            years: []
        },
        created() {
            this.updateCategoryCounts();
            this.updateYearCounts();
            //日付順に並び替え
            this.sortByDate(this.previous_newsData);
            this.sortByDate(this.newsData);
            this.selectedNews = [...this.previous_newsData];
        },
        methods: {
            updateCategoryCounts() {
                var categories = new Set(this.newsData.map(news => news[3]));
                this.categories = Array.from(categories).map(category => ({
                    name: category,
                    count: this.newsData.filter(news => news[3] === category).length
                }));
            },
            updateYearCounts() {
                var years = new Set(this.previous_newsData.map(news => news[6]));
                this.years = Array.from(years).map(year => ({
                    year: year,
                    count: this.previous_newsData.filter(news => news[6] === year).length
                })).sort((a, b) => b.year - a.year);
            },

            selectCategory(category) {
                this.selectedNews = this.newsData.filter(news => news[3] === category);
            },
            selectYear(year) {
                this.selectedNews = this.previous_newsData.filter(news => news[6] === year);
            },
            sortByDate(data) {
                data.sort((a, b) => {
                    const dateA = new Date(a[5].split('-').map(num => num.padStart(2, '0')).join('-'));
                    const dateB = new Date(b[5].split('-').map(num => num.padStart(2, '0')).join('-'));
                    return dateB - dateA;
                });
            },
            searchNewsByApps() {
                const data = JSON.stringify(this.selectedApps);
                fetch('http://localhost:5000/search', {
                    method: 'POST',
                    headers: {
                        "Content-Type": 'application/json',
                    },
                    body: data,
                })
                .then(response => response.json())
                .then(data => {
                    //データプロパティを更新
                    this.newsData = data.filtered_new_data;
                    this.appsData = data.filtered_apps;
                    this.previous_newsData = data.filtered_previous_data;
                    this.selectedNews = data.filtered_previous_data;
                    //更新したデータを日付順に並び替え
                    this.sortByDate(this.newsData);
                    this.sortByDate(this.previous_newsData);
                    this.sortByDate(this.selectedNews);
                    this.updateCategoryCounts();
                    this.updateYearCounts();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
                this.showModal = false;
                this.displayApps = this.selectedApps.join(', ');
            },
            toggleModal() {
                this.showModal = !this.showModal;
            },
            cancelSearch() {
                this.showModal = false;
            }
        }
    });
});

