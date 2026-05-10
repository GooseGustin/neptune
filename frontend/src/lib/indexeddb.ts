import { openDB, type IDBPDatabase } from 'idb'
import type { GeneratedModule } from '@/types/content'

const DB_NAME = 'neptune_content'
const DB_VERSION = 1
const STORE = 'modules'

let db: IDBPDatabase | null = null

async function getDB() {
  if (!db) {
    db = await openDB(DB_NAME, DB_VERSION, {
      upgrade(database) {
        if (!database.objectStoreNames.contains(STORE)) {
          const store = database.createObjectStore(STORE, { keyPath: 'module_id' })
          store.createIndex('course_id', 'course_id')
        }
      },
    })
  }
  return db
}

export async function saveModule(courseId: string, module: GeneratedModule): Promise<void> {
  const database = await getDB()
  await database.put(STORE, { ...module, course_id: courseId, saved_at: new Date().toISOString() })
}

export async function getModule(moduleId: string): Promise<GeneratedModule | null> {
  const database = await getDB()
  const record = await database.get(STORE, moduleId)
  return record ?? null
}

export async function getCourseModules(courseId: string): Promise<GeneratedModule[]> {
  const database = await getDB()
  const records = await database.getAllFromIndex(STORE, 'course_id', courseId)
  return records
}

export async function deleteModulesByCourse(courseId: string): Promise<void> {
  const database = await getDB()
  const records = await database.getAllFromIndex(STORE, 'course_id', courseId)
  const tx = database.transaction(STORE, 'readwrite')
  await Promise.all(records.map((r) => tx.store.delete(r.module_id)))
  await tx.done
}
