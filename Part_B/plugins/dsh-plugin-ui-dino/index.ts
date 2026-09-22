import { Context, Schema } from 'cordis'

export const name = 'dsh-plugin-ui-dino'

export interface Config {
  position: string
  sprite: string
}

export const Config: Schema<Config> = Schema.object({
  position: Schema.union(['bottom-right', 'bottom-left', 'top-right', 'top-left']).default('bottom-right').description('Position on the screen.'),
  sprite: Schema.string().default('dino.png').description('Sprite image for the dinosaur.')
})

export function apply(ctx: Context, config: Config) {
  ctx.logger.info('Injecting Dino UI plugin...')

  // Assuming `ctx.web` or `ctx.ui` exists in DeepSeek Harness to inject custom UI components
  // We'll mock the injection logic here.
  ctx.on('ready', () => {
    // This event fires when the plugin system is fully loaded
    ctx.logger.info(`Dino jumping game widget mounted at ${config.position} with sprite ${config.sprite}`)
    
    // In a real plugin, this would inject a script tag or iframe into the Web UI:
    /*
      ctx.ui.inject(`
        <div id="dino-widget" style="position: fixed; ${config.position}: 20px; z-index: 9999;">
          <img src="${config.sprite}" alt="Jumping Dino" width="50" class="dino-animate" />
          <script>
             console.log("Dino widget active!");
             // Game logic here
          </script>
        </div>
      `)
    */
  })
}
