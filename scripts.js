document.addEventListener('DOMContentLoaded', function () {
    var newsDataElement = document.getElementById('news-data');
    var newsData = JSON.parse(newsDataElement.textContent);


    new Vue({
        el: '#app',
        delimiters: ['${', '}'], // Vue.jsのデリミタを変更
        data: {
            newsData: newsData.news,
            appsData: newsData.apps,
            selectedNews: [],
            showModal: false,
            displayApps: '',
            categories: [], // カテゴリデータの初期化
            years: [] // 年データの初期化
        },
        created() {
            this.updateCategoryCounts();
            this.updateYearCounts();

        },
        methods: {
            updateCategoryCounts() {
                var categories = new Set(this.newsData.map(news => news.category));
                this.categories = Array.from(categories).map(category => ({
                    name: category,
                    count: this.newsData.filter(news => news.category === category).length
                }));
            },
            updateYearCounts() {
                var years = new Set(this.newsData.map(news => news.year));
                this.years = Array.from(years).map(year => ({
                    year: year,
                    count: this.newsData.filter(news => news.year === year).length
                }));
            },
            selectCategory(category) {
                this.selectedNews = this.newsData.filter(news => news.category === category);
            },
            selectYear(year) {
                this.selectedNews = this.newsData.filter(news => news.year === year);
            },
            searchNewsByApps() {
                this.selectedNews = this.news.filter(news => this.selectedApps.includes(news.app));
                this.showModal = false;
                this.updateCategoryCounts();
                this.updateYearCounts();
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
