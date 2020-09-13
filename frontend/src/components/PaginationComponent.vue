<template>
    <div id="pagination">
        <a class="arrow arrow-left"
             @click="changePage(prevPage)"
             :class="hasPrev() ? '' : 'disabled'"
        >
            <svg width="10" height="13" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5.25921 2.25921L1.4715 5.1C1.20484 5.3 1.20484 5.7 1.4715 5.9L5.25921 8.74079" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </a>
        <a :class="current == 1 ? 'current' : ''"
           v-if="hasFirst"
           @click="changePage(1)"
        >
            <span>1</span>
        </a>
        <i v-if="current > 3" class="ellipsis">..</i>
        <a :class="page == current ? 'current' : ''"
            v-for="page in pages"
            @click="changePage(page)"

        >
            <span>{{page}}</span>
        </a>
        <i class="ellipsis" v-if="current < (count-2)">..</i>
        <a :class="current == count ? 'current' : ''"
           v-if="hasLast"
           @click="changePage(count)"
        >
            <span>{{count}}</span>
        </a>

        <a class="arrow arrow-right"
             @click="changePage(nextPage)"
             :class="hasNext() ? '' : 'disabled'"
        >
            <svg width="10" height="13" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4.74081 2.25919L8.52856 5.1C8.79523 5.3 8.79523 5.7 8.52856 5.9L4.74081 8.74081" stroke="#0057B6" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </a>
    </div>
</template>

<script>
export default {
    name: "PaginationComponent",
    props: {
        current: {
            type: Number,
            default: 1
        },
        count: {
            type: Number
        },

    },
    data(){
        return {
            currentPagePagination: 0,
            listNumPages: [1,2,3],
            lastPagePagination: 7,
        }
    },
    computed: {
        nextPage(){
            return this.current + 1;
        },
        prevPage(){
            return this.current - 1;
        },
        hasFirst(){
            return this.rangeStart !== 1;
        },
        hasLast(){
            return this.rangeEnd < this.count;
        },
        rangeStart(){
            let start = this.current - 1;
            return (start > 0) ? (this.current === this.count && start - 1 > 0) ? start - 1 : start : 1;
        },
        rangeEnd(){
            let end = this.current + 1;
            return (end < this.count) ? (this.current === 1) && (end + 1 <= this.count) ? end + 1 : end : this.count;
        },
        pages() {
            let pages = [];

            for(let i = this.rangeStart; i <= this.rangeEnd; i++){
                pages.push(i);
            }

            return pages;
        }
    },
    methods: {
        hasPrev(){
            return this.current > 1;
        },
        hasNext(){
            return this.current < this.count;
        },
        changePage(page) {
            this.$emit('page-changed', page);
        }
    }
}
</script>

<style lang="scss" scoped>

@import "../styles_fonts";
$font-Inter: Inter, 'Inter';


#pagination {
    height: 37px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 210px;
    user-select: none;

    .disabled {
        opacity: .3;
        pointer-events: none;
        cursor: default;
    }

    .ellipsis {
        transition: all .5s;
        pointer-events: none;
        cursor: default;
    }

    a {
        background: #FFFFFF;
        border: 1.5px solid #E6E6E6;
        box-sizing: border-box;
        border-radius: 4px;
        margin: 0 2.5px;
        min-width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all .3s;

        span {
            font-family: $font-Inter;
            font-style: normal;
            font-weight: normal;
            font-size: 13px;
            color: #0057B6;
            border-radius: 4px;
        }

        &:hover {
            background: #CEDFF4;
        }
    }


    .arrow {
        height: 30px;
        width: 30px;
        min-width: auto;
        cursor: pointer;


        svg {
            width: 10px;
            height: 11px;
        }
    }

    .current {
        background: #CEDFF4;
    }
}

</style>