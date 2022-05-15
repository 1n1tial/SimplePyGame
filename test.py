def meteor_hit_action(group):
    hits = pygame.sprite.groupcollide(group, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 5
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        if group == meteors_large:
            spawn_med_mob(hit.rect.centerx, hit.rect.centery)
            spawn_med_fake_mob(hit.rect.centerx, hit.rect.centery)
        elif group == meteors_med:
            spawn_small_mob(hit.rect.centerx, hit.rect.centery)
            spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
        elif group == meteors_fake_med:
            spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
            spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
        elif group == meteors_small:
            spawn_meteor_top()
        elif group == meteors_fake_small:
            pass
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

hits = pygame.sprite.groupcollide(meteors_large, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 5
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "large")
        all_sprites.add(expl)
        spawn_med_mob(hit.rect.centerx, hit.rect.centery)
        spawn_med_fake_mob(hit.rect.centerx, hit.rect.centery)
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.groupcollide(meteors_med, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 8
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "large")
        all_sprites.add(expl)
        spawn_small_mob(hit.rect.centerx, hit.rect.centery)
        spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.groupcollide(meteors_fake_med, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 8
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "large")
        all_sprites.add(expl)
        spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
        spawn_small_fake_mob(hit.rect.centerx, hit.rect.centery)
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.groupcollide(meteors_small, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 15
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "large")
        all_sprites.add(expl)
        spawn_meteor_top()
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.groupcollide(meteors_fake_small, bullets, True, True)
    for hit in hits:
        score += 5
        player.fuel += 15
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "large")
        all_sprites.add(expl)
        if random.random() > 1 - powerup_spawn_rate:
            pow = PowerUp(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)