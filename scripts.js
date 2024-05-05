new Vue({
    el: '#app',
    data: {
        news: [
            { id: 1, title: 'Vue.js 3.0 リリース', content: 'Vue.jsの新バージョンがリリースされました。', category: 'Technology', year: '2023', app: 'Vue.js', registration: '2023/03/01' },
            { id: 2, title: 'Bootstrap 5 リリース', content: 'Bootstrap 5が公開されました。', category: 'Design', year: '2022', app: 'Bootstrap', registration: '2022/05/20' },
            { id: 3, title: '新機能アップデート', content: '新機能が追加されました。', category: 'Announcement', year: '2023', app: 'General', registration: '2023/01/15' },
            { id: 4, title: '年末のお知らせ', content: '年末のスケジュールについて。', category: 'Announcement', year: '2022', app: 'General', registration: '2022/11/30' },
            { id: 5, title: 'システムメンテナンス通知', content: 'システムメンテナンスを行います。', category: 'Maintenance', year: '2023', app: 'System', registration: '2023/02/11' },
            { id: 6, title: '重要なお知らせ', content: '利用規約が更新されます。', category: 'お知らせ', year: '2023', app: 'General', registration: '2023/04/01' },
            { id: 7, title: 'AutoCADバージョンアップ', content: 'AutoCADの新バージョンがリリースされました。', category: 'お知らせ', year: '2024', app: 'Autodesk', registration: '2024/04/12' }
        ],
        years: [],
        categories: [],
        selectedNews: [],
        apps: [
            { name: '共通' },
            { name: 'Vue.js' },
            { name: 'Bootstrap' },
            { name: 'Autodesk' }
        ],
        selectedApps: [],
        showModal: false,
        displayApps: ''
    },
    created() {
        this.updateCategoryCounts();
        this.updateYearCounts();
        this.selectCategory('お知らせ');
    },
    methods: {
        updateCategoryCounts() {
            this.categories = this.news.map(news => news.category)
                                        .filter((value, index, self) => self.indexOf(value) === index)
                                        .map(category => ({
                                            name: category,
                                            count: this.news.filter(news => news.category === category).length
                                        }));
        },
        updateYearCounts() {
            let years = this.news.map(news => news.year)
                                 .filter((value, index, self) => self.indexOf(value) === index)
                                 .sort((a, b) => b - a); // Sort years in descending order
            this.years = years.map(year => ({
                year: year,
                count: this.news.filter(news => news.year === year).length
            }));
        },
        selectCategory(category) {
            this.selectedNews = this.news.filter(news => news.category === category);
        },
        selectYear(year) {
            this.selectedNews = this.news.filter(news => news.year === year);
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
