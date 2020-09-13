<template>
    <div id="filter">
        <h3 class="filter-head">Фильтры</h3>
        <div class="filters-list">
            <!--<div class="filter-item">
                <div class="filter-title" @click="typesFilters[1] = !typesFilters[1]">
                    <span>По ID клиента</span>
                    <svg :style="typesFilters[1] ? {'transform': 'scale(1, -1)'} : ''" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="filter-options"  v-if="typesFilters[1]">
                    <div class="option" v-for="opt in 10">
                        <label :for="'inpt'+opt" class="option">Клиент № {{opt}}</label>
                        <input :id="'inpt'+opt" type="checkbox">
                    </div>
                </div>
            </div>-->
            <div class="filter-item">
                <div class="filter-title" @click="typesFilters[2] = !typesFilters[2]">
                    <span>Тип POI</span>
                    <svg :style="typesFilters[2] ? {'transform': 'scale(1, -1)'} : ''" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="filter-options"  v-if="typesFilters[2]">
                    <div class="option" v-for="(poi,i) in poiTypes" @click="setFilter">
                        <label :for="'inpt'+i" class="option">{{poi.name}}</label>
                        <input :id="'inpt'+i" v-model="poi.active" type="checkbox">
                    </div>
                </div>
            </div>
            <div class="filter-item">
                <input class="find-input" type="text" placeholder="ID Клиента" v-model="textSearch" @input="findUsers">
            </div>
            <!--<div class="filter-item">
                <div class="filter-title" @click="typesFilters[3] = !typesFilters[3]">
                    <span>Степень вовлеченности</span>
                    <svg :style="typesFilters[3] ? {'transform': 'scale(1, -1)'} : ''" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="filter-options"  v-if="typesFilters[3]">
                    <div class="option" v-for="opt in 10">
                        <label :for="'inpt'+opt" class="option">Клиент № {{opt}}</label>
                        <input :id="'inpt'+opt" type="checkbox">
                    </div>
                </div>
            </div>
            <div class="filter-item">
                <div class="filter-title" @click="typesFilters[4] = !typesFilters[4]">
                    <span>Расстояние до POI</span>
                    <svg :style="typesFilters[4] ? {'transform': 'scale(1, -1)'} : ''" width="11" height="11" viewBox="0 0 11 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.24629 5.35536L5.56933 9.03231C5.45217 9.14947 5.26222 9.14947 5.14507 9.03231L1.21321 5.10045" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="filter-options"  v-if="typesFilters[4]">
                    <div class="option" v-for="opt in 5">
                        <label :for="'inpt'+opt" class="option">Клиент № {{opt}}</label>
                        <input :id="'inpt'+opt" type="checkbox">
                    </div>
                </div>
            </div>-->
        </div>
    </div>
</template>

<script>
export default {
    name: "FilterComponent",
    data(){
        return {
            textSearch: '',
            typesFilters: {
                2: true,
            },
            poiTypes: [
                {
                    name: 'Заправочные станции',
                    id: 1,
                    active: true
                },
                {
                    name: 'Стройки партнеров',
                    id: 2,
                    active: true
                },
                {
                    name: 'Отделения Банков',
                    id: 3,
                    active: true
                },
            ]
        }
    },
    methods: {
        findUsers(){
            this.$emit('textEntered', this.textSearch);
        },
        setFilter(ind){
            setTimeout(() => {
                this.$emit('setFilter', this.poiTypes);
            })
        }
    }
}
</script>

<style scoped lang="scss">

@import "../styles_fonts";
$font-Inter: Inter, 'Inter';

#filter {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.filter-head {
    font-family: $font-Inter;
    font-style: normal;
    font-weight: 500;
    font-size: 16px;
    line-height: 200%;
    color: #A0A0A0;
}

.filters {
    width: 100%;
    display: flex;
    flex-direction: column;

    .filter-item {
        width: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 12px;

        .find-input {
            padding: 5px 10px;
            border-radius: 4px;
            width: 80%;
            margin-top: 12px;
            border: 1px solid #727272;
            font-family: $font-Inter;
            font-style: normal;
            font-weight: normal;
            font-size: 16px;
            line-height: 150%;
            color: #262C40;


            &:focus {
                outline: none;
            }
        }

        .filter-title, .option {
            span, label {
                margin: 0;
                font-family: $font-Inter;
                font-style: normal;
                font-weight: normal;
                font-size: 16px;
                line-height: 150%;
                color: #262C40;
            }


            svg {
                margin-left: 12px;
                width: 11px;
                height: 11px;
                display: inline-block;
            }
        }


        .filter-title {
            width: 80%;
            cursor: pointer;
            user-select: none;
            align-items: center;
            display: flex;
            justify-content: space-between;

            svg {
                transition: all .3s;
            }
        }

        .filter-options {
            width: calc(100% - 20px - 20%);
            margin-left: 20px;
            animation: anim .3s ease;
            //margin-top: 10px;

            .option {
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all .4s;
                margin: 5px 0 0 0;

                &:hover {
                    color: #2a84e9;
                }

                label {
                    font-size: 15px;
                    user-select: none;
                }

                input {
                    margin: 0 0 0 11px;
                    padding: 3px;
                    border-color: #0057B6;
                }
            }
        }

    }
}

@keyframes anim {
    0% {
        opacity: 0;
        transform: scaleY(0) translateY(-50%);
    }

    100% {
        transform: scaleY(1);
    }
}

</style>