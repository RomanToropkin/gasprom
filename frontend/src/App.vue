<template>
    <div id="app">
        <div class="wrapper">
            <FilterComponent class="filters"
                @setFilter="setFilter" @textEntered="setTextSearch"
            >

            </FilterComponent>
            <div class="table-wrap">
                <div class="mobile-table" v-if="mobileVersion">
                    <div class="mobile-cell" v-for="client in 5">
                        <div class="mobile-prop"
                             v-for="(h,i) in headers"
                        >
                            <p  class="prop-title">{{h}}</p>
                            <p class="prop-value">{{clients[0][Object.keys(clients[0])[i]]}}</p>
                        </div>
                    </div>
                </div>
                <div class="table-clients" v-else>
                    <div class="table-head">
                        <p class="table-head-cell table-cell">
                            <i>ID клиента</i>
                        </p>
                        <p class="table-head-cell table-cell">
                            <i>Тип POI</i>
                        </p>
                        <p class="table-head-cell table-cell">
                            <i>Координаты POI</i>
                        </p>
                        <p :class="order == 'speed' ? 'active' : ''" class="table-head-cell table-cell clickable" @click="setSort('speed')">
                            <i>Скорость (</i>км/ч)
                            <svg :class="order == 'speed' ? order_type ? 'translated-ico' : ''  : 'hidden-ico'" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#A0A0A0" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                        </p>
                        <p :class="order == 'dist' ? 'active' : ''" class="table-head-cell table-cell clickable" @click="setSort('dist')">
                            <i>Расстояние (м)</i>
                            <svg :class="order == 'dist' ? order_type ? 'translated-ico' : ''  : 'hidden-ico'" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#A0A0A0" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                        </p>
                        <p :class="order == 'date' ? 'active' : ''" class="table-head-cell table-cell clickable" @click="setSort('date')">
                            <i>Время</i>
                            <svg :class="order == 'date' ? order_type ? 'translated-ico' : ''  : 'hidden-ico'" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#A0A0A0" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                        </p>
                    </div>
                    <div class="table-content">
                        <transition name="appear"
                                    v-for="(client,index) in clients"
                                    :key="index"
                        >
                            <div class="table-row"
                                 v-show="showingTable"
                            >
                                <p class="table-cell">
                                    {{client.id_client}}
                                </p>

                                <p class="table-cell">
                                    {{client.name}}
                                </p>


                                <p class="table-cell">
                                    ш. {{client.lat}}
                                    <br>
                                    д. {{client.lon}}
                                </p>

                                <p class="table-cell">
                                    {{Math.ceil((client.speed)*100)/100}}
                                </p>

                                <p class="table-cell">
                                    {{client.dist}}
                                </p>

                                <p class="table-cell" v-if="client.date">
                                    {{client.date.split(' ')[1]}}
                                    <br>
                                    {{client.date.split(' ')[0]}}
                                </p>


                            </div>
                        </transition>
                    </div>
                </div>
                <div class="pagination-wrap">
                    <PaginationComponent
                        @page-changed="changeCurrentPage"
                        :current="currentPage"
                        :count="parseInt(countPages)"
                    ></PaginationComponent>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PaginationComponent from "./components/PaginationComponent";
import FilterComponent from "./components/FilterComponent";
import axios from 'axios';

export default {
    name: 'app',
    components: {
        PaginationComponent,
        FilterComponent
    },
    data(){
        return {
            showingTable: false,
            currentPage: 1,
            countPages: 1,
            poiFilters: '',
            textSearch: '',
            mobileVersion: false,
            headers: [
                'ID клиента',
                'Тип POI',
                'Координаты POI',
                'Скорость (км/ч)',
                'Расстояние (м)',
                'Время'
            ],
            clients: [
                {
                    id: 'Анатолий Вассерман Возанович',
                    type_poi: 'Отделение банка банковское отделение банка',
                    coords: '55.554771 ш., 37.924931 д.',
                    percents: 89,
                    distance: 769
                }
            ],
            order: 'date',
            order_type: 0
        }
    },
    created() {
        this.$nextTick(function() {
            window.addEventListener('resize', this.getWindowWidth);
            this.getWindowWidth();
        });
        this.getEvents();
        setInterval(() => {
            this.getEvents();
        }, 10000)

    },
    methods: {
        setTextSearch(text){
            this.textSearch = text;
            this.getEvents();
        },
        setSort(order){
            this.currentPage = 1;
            if(this.order == order){
                this.order_type = !this.order_type
            } else {
                this.order = order;
                this.order_type = 0;
            }
            this.getEvents();
        },
        setFilter(poiTypes){
            this.currentPage = 1;
            let res = '';
            poiTypes.forEach((poi) => {
                if(poi.active){
                    res += '&filter[]='+poi.id;
                }
            });
            this.poiFilters = res;
            this.getEvents();
        },
        getEvents(){
            let asc = this.order_type ? 'DESC' : 'ASC';
            axios.get('https://franq.creativityprojectcenter.ru/api/api.php?type=getEvents'+
                '&page='+this.currentPage +
                '&order='+this.order+
                '&order_type='+asc+
                '&query='+this.textSearch+
                this.poiFilters
            )
                .then(res => {
                    this.countPages = res.data.page_count;
                    this.clients = res.data.data;
                    this.showingTable = true;
                })
        },
        changeCurrentPage(page){
            this.currentPage = page;
            this.getEvents();
        },
        getWindowWidth(event) {
            this.mobileVersion = document.documentElement.clientWidth < 768;
        },
    }
}
</script>

<style lang="scss" scoped>
html, body {
    margin: 0;
    padding: 0;
}

ul {
    list-style-type: none;
}

li {
    list-style: none;
    display: flex;
}

#down_header .hooper-slide {
    text-align: center;
    display: flex;
    justify-content: center;

}

@import "./styles_fonts";
$font-Inter: Inter, 'Inter';

#app {
    width: 100vw;
    height: auto;
}


.wrapper {
    display: flex;
    width: calc(100% - 120px);
    margin: 50px auto;
}
.filters {
    width: 20% !important;
}


.table-wrap {
    width: 80%;
    display: flex;
    flex-direction: column;
    transition: all 1.5s;

    .table-clients {
        transition: all 1.5s;
        width: 100%;

        .table-head, .table-content .table-row {
            display: grid;
            grid-template-columns: .8fr 1.3fr 1.1fr 1.2fr 1.1fr .9fr;
            display: -ms-grid;
        }

        .table-head {
            width: 100%;

            .table-head-cell {
                display: flex;
                align-items: center;
                user-select: none;

                i {
                    font-style: normal;
                    font-weight: bold;
                }
                svg {
                    transition: all .3s;
                    margin: 0 0 0 7px;
                }

                .hidden-ico {
                    opacity: .2;
                }

                .translated-ico {
                    transform: scaleY(-1);
                }
            }

            .clickable {
                transition: all .4s;
                cursor: pointer;

                &:hover {
                    color: #2b2b2b;
                }
            }

            .active {
                color: #2b2b2b;
            }

            .table-cell {

            }
        }

        .table-row {
            border-radius: 20px;
        }

        .table-row:nth-child(odd) {
            background: #F5F5F5;
        }

        .table-cell {
            //text-align: center;
            max-width: 100%;
            padding: 0 10px;
            font-family: $font-Inter;
            font-style: normal;
            font-weight: normal;
            font-size: 16px;
            line-height: 130%;
            color: #A0A0A0;
        }
    }

    .mobile-table {
        display: flex;
        flex-direction: column;
        grid-gap: 20px;

        .mobile-cell {
            border-radius: 20px;

            .mobile-prop {
                display: flex;
                justify-content: space-between;

                p {
                    padding: 0 12px;
                    margin: 10px 0;
                    font-family: $font-Inter;
                    font-style: normal;
                    font-weight: normal;
                    font-size: 16px;
                    line-height: 130%;
                    color: #262C40;

                }

                .prop-title {
                    font-weight: 600;
                    width: 40%;
                }

                .prop-value {
                    width: 60%;
                }
            }


            &:nth-child(odd){
                background: #F5F5F5;
            }
        }
    }

    .pagination-wrap {
        justify-content: flex-end;
        width: 100%;
        display: flex;
        margin-top: 10px;
    }
}

@media (max-width: 767px) {

    .wrapper {
        display: flex;
        width: calc(100% - 60px);
        margin: 100px auto;

    }

    .table-wrap {
        width: 100%;
    }
}

.appear-height-enter-active {
    transition: all 1.85s;
}
.appear-height-enter {
    opacity: 0;
    transform: scaleY(0);
}

.appear-enter-active {
    transition: opacity 1s;
}
.appear-enter {
    opacity: 0;
}

</style>
