import { createRouter, createWebHistory } from 'vue-router'
import main from '../views/main/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'man',
      component: main
    },
    {
      path: '/topic',
      name: 'topic',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/topic/index.vue')
    },
    {
      path: '/searchUser',
      name: 'searchUser',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/searchUser/index.vue')
    },
    {
      path: '/searchTopic',
      name: 'searchTopic',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/searchTopic/index.vue')
    },
    {
      path: '/more',
      name: 'more',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/components/alltopicpage/index.vue')
    },
    {
      path: '/some_topic',
      name: 'cxkcxkcxkcxk',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/cxktopic/index.vue')
    }
  ]
})

export default router
