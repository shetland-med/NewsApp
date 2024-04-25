new Vue({
    el: '#app',
    data: {
        news: [
            { id: 1, title: 'Vue.js 3.0 リリース', content: 'Vue.jsの新バージョンがリリースされました。', category: 'Technology', year: '2023', app: 'Vue.js', registration: '2023/03/01' },
            { id: 2, title: 'Bootstrap 5 リリース', content: 'Bootstrap 5が公開されました。', category: 'Design', year: '2022', app: 'Bootstrap', registration: '2022/05/20' },
            { id: 3, title: '新機能アップデート', content: '新機能が追加されました。', category: 'Announcement', year: '2023', app: 'General', registration: '2023/01/15' },
            { id: 4, title: '年末のお知らせ', content: '年末のスケジュールについて。', category: 'Announcement', year: '2022', app: 'General', registration: '2022/11/30' },
            { id: 5, title: 'システムメンテナンス通知', content: 'システムメンテナンスを行います。', category: 'メンテナンス', year: '202', app: '共通', registration: '2023/02/11' },
            { id: 6, title: '重要なお知らせ', content: '利用規約が更新されます。', category: 'お知らせ', year: '2023', app: 'General', registration: '2023/04/01' },
            { id: 7, title: 'AutoCADバージョンアップ', content: 'AutoCADの新バージョンがリリースされました。', category: 'お知らせ', year: '2024', app: 'Autodesk', registration: '2024/04/12' }
        ],
        years: ['2024', '2023', '2022'],
        categories: [
            { name: 'お知らせ', count: 0 },
            { name: 'メンテナンス', count: 0 },

        ],
        selectedNews: [],
        apps: [
            { name: '共通' },
            { name: 'Vue.js' },
            { name: 'Bootstrap' },
            { name: 'Autodesk' }
        ],
        selectedApps: [],
        showModal: false
    },
    created() {
        this.updateCategoryCounts();
        this.updateYearCounts();
    },
    methods: {
        updateCategoryCounts() {
            this.categories.forEach(category => {
                category.count = this.news.filter(news => news.category === category.name).length;
            });
        },
        updateYearCounts() {
            this.years.forEach(year => {
                this.$set(this, year, this.news.filter(news => news.year === year).length);
            });
        },
        countNewsByYear(year) {
            return this.news.filter(item => item.year === year).length;
        },
        countNewsByCategory(categoryName) {
            return this.news.filter(item => item.category === categoryName).length;
        },
        selectCategory(category) {
            this.selectedNews = this.news.filter(item => item.category === category);
            this.updateCategoryCounts();
        },
        selectYear(year) {
            this.selectedNews = this.news.filter(item => item.year === year);
            this.updateYearCounts();
        },
        searchNewsByApps() {
            this.selectedNews = this.news.filter(item => this.selectedApps.includes(item.app));
            this.showModal = false;
            this.updateCategoryCounts();
            this.updateYearCounts();
        },
        toggleModal() {
            this.showModal = !this.showModal;
            if (!this.showModal) {
                this.originalSelectedApps = [...this.selectedApps];
            }
        },
        cancelSearch() {
            this.selectedApps = [...this.originalSelectedApps];
            this.selectedNews = [];
            this.showModal = false;
            this.updateCategoryCounts();
            this.updateYearCounts();
        }
    }
});
