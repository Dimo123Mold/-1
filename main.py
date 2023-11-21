from objects import *

finish = True
pause = False
game = False

player = Player(player_image, 350, 250, 100, 100, 5)

for i in range (15):
    e = Enamy(dog_image[0], 100, 100, 50, 50, 2 )
    e.spawn()
    enamys.add(e)


def callback_start():
    global finish, game, player, enamy, boss, score, level
    boss = False
    finish = False
    game = True
    score = 0
    level = 0
    player = Player(player_image, 350, 250, 100, 100, 5)
    enamys.empty()
    for i in range (15):
        e = Enamy(dog_image[0], 100, 100, 50, 50, 2 )
        e.spawn()
        enamys.add(e)

bt_start = Button(win_width / 2, 100, 150, 50, (50, 50, 100), bt_start_text, callback_start)
bt_exit = Button(win_width / 2, 400, 150, 50, (50, 50, 100), bt_exit_text, exit)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    if finish:
        win.blit(main_background_image, (0, 0))
        bt_start.update()
        bt_start.draw()
        bt_exit.update()
        bt_exit.draw()

    if game:
        win.blit(background_image, (0, 0))
        for enamy in enamys:
            dx = enamy.rect.centerx - player.rect.centerx
            dy = player.rect.centery - enamy.rect.centery
            ang = -math.atan2(dy, dx) - math.pi
            enamy.update(ang)
            enamy.draw()
            if player.hitbox.colliderect(enamy.hitbox):

                player.hp -= enamy.damage
                if enamy.max_hp == 15:
                    enamy.kill()
                    boss = False
                else:
                    enamy.spawn()
        colllade = pygame.sprite.groupcollide(enamys, bullets, False, True)

        for enamy in colllade:    
            enamy.hp -= 1
            if enamy.hp <= 0:
                if enamy.max_hp == 15:
                    enamy.kill()
                    score += 10
                    boss = False
                else:
                    enamy.spawn()
                    score += 1


        player.update()
        player.draw()
        bullets.update()
        bullets.draw(win)

        if score % 15 == 0 and score != 0  and not boss:
            boss1 = Enamy(dog_image[0], - 100, -200, 120, 120, 2)
            boss1.max_hp = 10
            boss1.spawn()
            enamys.add(boss1)
            boss  = True

        if score % 30 == 0 and score != 0:
            score += 1
            level += 1
            for enamy in enamys:
                if enamy.max_hp != 15:
                    enamy.max_hp += 1
                    enamy.damage += 1
                if level in(6, 9):
                    enamy.speed  += 1

        pygame.draw.rect(win, bac, UI)

        hel = ui_d.render(f"HP: {player.hp}/100",
                          True,
                          (255, 50, 50))
        win.blit(hel, (0, win_height + 5))

        scores = ui_d.render(f"Score: {score}",
                          True,
                          (255, 50, 50))
        win.blit(scores, (500, win_height + 5))

        if player.hp <= 0:
            game = False
            finish = True
            lose_text = ui_d.render(f"Dead", True, (0, 0, 0))

    pygame.display.update()
    clock.tick(FPS)
    
