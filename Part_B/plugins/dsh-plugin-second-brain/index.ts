import { Context, Schema } from 'cordis'
import * as fs from 'fs'
import * as path from 'path'

export const name = 'dsh-plugin-second-brain'

export interface Config {
  storagePath: string
  syncInterval: number
}

export const Config: Schema<Config> = Schema.object({
  storagePath: Schema.string().default('./knowledge_base').description('Path to store knowledge base markdown files.'),
  syncInterval: Schema.number().default(60).description('Interval in seconds to sync data.')
})

export function apply(ctx: Context, config: Config) {
  ctx.logger.info(`Starting Second Brain plugin. Storage path: ${config.storagePath}`)

  // Ensure storage directory exists
  if (!fs.existsSync(config.storagePath)) {
    fs.mkdirSync(config.storagePath, { recursive: true })
  }

  // Listen to agent insights/events (mocked for this assignment)
  ctx.on('agent/insight', (insight: string, topic: string) => {
    const filename = `${topic.replace(/\s+/g, '_').toLowerCase()}.md`
    const filepath = path.join(config.storagePath, filename)
    
    const content = `## Insight: ${topic}\n\n${insight}\n\n*Recorded at ${new Date().toISOString()}*\n`
    fs.appendFileSync(filepath, content, 'utf8')
    ctx.logger.info(`Saved insight to ${filepath}`)
  })

  // Timer for sync
  ctx.setInterval(() => {
    ctx.logger.debug('Syncing second brain to disk...')
    // Perform sync operations
  }, config.syncInterval * 1000)
}
