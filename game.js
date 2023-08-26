const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

let paddle;
let ball;
let blocks;
let cursors;
let game = new Phaser.Game(config);

function preload() {
    // 必要なリソースを事前に読み込む
}

function create() {
    // パドルの作成
    paddle = this.physics.add.rectangle(400, 590, 100, 20, 0x00FF00).setImmovable();
    cursors = this.input.keyboard.createCursorKeys();

    // ボールの作成
    ball = this.physics.add.circle(400, 300, 7.5, 0xFF0000);
    ball.setVelocity(Phaser.Math.Between(-150, 150), -150);
    ball.setCollideWorldBounds(true);
    ball.setBounce(1);

    // ブロックの作成
    blocks = this.physics.add.staticGroup({
        key: 'block',
        repeat: 49,
        setXY: { x: 40, y: 30, stepX: 82, stepY: 40 }
    });
    this.physics.add.collider(ball, blocks, hitBlock, null, this);
    this.physics.add.collider(ball, paddle, hitPaddle, null, this);
}

function update() {
    if (cursors.left.isDown) {
        paddle.setVelocityX(-350);
    } else if (cursors.right.isDown) {
        paddle.setVelocityX(350);
    } else {
        paddle.setVelocityX(0);
    }

    if (ball.y > this.sys.game.config.height) {
        gameOver();
    }
}

function hitBlock(ball, block) {
    block.disableBody(true, true);

    if (blocks.countActive(true) === 0) {
        winGame();
    }
}

function hitPaddle(ball, paddle) {
    ball.setVelocityY(ball.body.velocity.y * -1);
}

function gameOver() {
    console.log("ゲームオーバー！");
    this.physics.pause();
    ball.setTint(0xff0000);
}

function winGame() {
    console.log("勝利！");
    this.physics.pause();
    ball.setTint(0x00ff00);
}
