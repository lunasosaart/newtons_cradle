"""
newtons_cradle.py
creates a working animated newtons cradle
by Luna Sosa
created: 10.24.23
last modified: 11.15.23

 ** find this code and more at lunasosaart.myportfolio.com/coding-for-maya ** 

MEANT TO WORK WITH MAYA 2022

NOTE: Video seen in portfolio contains an HDRI for the background via polyhaven.com.
This code is modified to include a skydome instead of the HDRI
Best seen through the Arnold renderview
"""

import maya.cmds as cmds

PFX = "LS_"

# MAIN #


def base():
    # create model
    curr = cmds.polyCube(n=f"{PFX}base_1", w=22, d=12)
    cmds.polyBevel()

    cmds.group(f"{PFX}base_1", n=f"{PFX}base_GRP")

    # create and apply shader
    base_obj_color = cmds.shadingNode('aiStandardSurface', n=f"{PFX}base_shd", asShader=True)
    cmds.setAttr(base_obj_color + ".baseColor", .5, .5, .5, type="double3")
    cmds.setAttr(base_obj_color + ".specular", 1)
    cmds.setAttr(base_obj_color + ".specularRoughness", 0.01)
    cmds.setAttr(base_obj_color + ".transmission", 1)
    cmds.setAttr(base_obj_color + ".opacity", .8, .8, .8, type="double3")
    cmds.select(curr)
    cmds.hyperShade(assign=base_obj_color)

    return curr


def beams():
    # create curve_1
    cmds.polyCylinder(n=f"{PFX}curve_1", sy=20, h=12, r=0.3)
    cmds.move(2.9, 5, 0)

    # bend curve_1
    cmds.nonLinear(type='bend', curvature=90, n=f"{PFX}bend01")
    cmds.rotate(0, 90, 0)
    cmds.scale(1, 1, 1, r=1)
    cmds.move(0, 0, 0)

    cmds.setAttr(f"{PFX}bend01.lowBound", 0)
    cmds.select(f"{PFX}curve_1")
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    cmds.select(f"{PFX}curve_1")
    cmds.move(6, 6.5, -4.5)
    cmds.rotate(0, 90, 0)

    # create curve_2
    cmds.duplicate(f"{PFX}curve_1")
    cmds.rotate(0, 270, 0)
    cmds.DeleteHistory()
    cmds.FreezeTransformations()
    cmds.move(-17.5, 0, 0)

    # create curve_3 and curve_4
    cmds.select(f"{PFX}curve_1", f"{PFX}curve_2")
    cmds.duplicate()
    cmds.DeleteHistory()
    cmds.FreezeTransformations()
    cmds.select(f"{PFX}curve_3", f"{PFX}curve_4")
    cmds.rotate(180, 0, 0)
    cmds.move(0, -12, 0)
    cmds.select(f"{PFX}curve_3")
    cmds.rotate(0, 90, 180)
    cmds.delete(f"{PFX}curve_3" + ".f[260:399]", f"{PFX}curve_3" + ".f[401]")
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    # create beam_02
    cmds.select(f"{PFX}curve_1", f"{PFX}curve_2", f"{PFX}curve_3", f"{PFX}curve_4")
    cmds.duplicate()
    cmds.DeleteHistory()
    cmds.FreezeTransformations()
    cmds.move(0, 0, 9)
    cmds.select(f"{PFX}curve_7")
    cmds.rotate(0, 180, 0)
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    # create connector beam
    cmds.select(f"{PFX}curve_3", f"{PFX}curve_7")
    cmds.duplicate()
    cmds.rotate(0, 0, 90)
    cmds.move(-2.682, 1.18, 0)
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    # group each beam and apply shader
    beam_grp = cmds.group(empty=True, n=f"{PFX}beam_GRP")
    beam_obj_color = cmds.shadingNode('aiStandardSurface', n=f"{PFX}beamShd", asShader=True)
    cmds.setAttr(beam_obj_color + ".metalness", .7)
    cmds.setAttr(beam_obj_color + ".specularRoughness", .14)
    cmds.setAttr(beam_obj_color + ".baseColor", .18, .05, .18)

    for i in range(10):
        beam = f"{PFX}curve_" + str(i + 1)
        cmds.parent(beam, beam_grp)
        cmds.select(f"{PFX}curve_" + str(i + 1))
        cmds.hyperShade(assign=beam_obj_color)

    return beam_grp


def balls():
    # create model
    for i in range(5):
        cmds.polySphere(r=1.3, n=f"{PFX}ball_" + str(i + 1))
        cmds.move(-5 + i * 2.6, 3, 0)

        # based on the 'how to model strawberry on Maya video' by 3dEx on Youtube
        # https://www.youtube.com/watch?v=jnHvxVBNRCA

        # make strawberry body
        cmds.softSelect(sse=True)
        cmds.select(f"{PFX}ball_" + str(i + 1) + ".f[26:39]", f"{PFX}ball_" + str(i + 1) + ".f[50:56]",
                    f"{PFX}ball_" + str(i + 1) + ".f[360:379]")
        cmds.scale(0.7, 1.5, 1)
        cmds.select(f"{PFX}ball_" + str(i + 1) + ".f[328: 338]", f"{PFX}ball_" + str(i + 1) + ".f[380:399]")
        cmds.scale(1.38, 1, 1)
        cmds.select(f"{PFX}ball_" + str(i + 1) + ".f[291:296]", f"{PFX}ball_" + str(i + 1) + ".f[308: 359]",
                    f"{PFX}ball_" + str(i + 1) + ".f[380: 399]")
        cmds.scale(1.03, 0.8, 1)
        cmds.softSelect(sse=False)

        # dimple strawberry
        straw = []
        for j in range(780):
            straw.append(f"{PFX}ball_{i + 1}.e[{j}]")
        cmds.polyPoke(f"{PFX}ball_" + str(i + 1))
        cmds.delete(straw)

        dimple = []
        for k in range(822):
            if k % 3 == 0:
                dimple.append(f"{PFX}ball_{i + 1}.vtx[{k}]")
        cmds.select(dimple)
        cmds.move(0, 0, -.07, relative=True)

        # make leaves
        cmds.polyCylinder(n=f"{PFX}leaf_" + str(i + 1))
        cmds.move(-5 + i * 2.6, 3.86, 0)

        cmds.select(f"{PFX}leaf_" + str(i + 1) + ".f[0:39]")
        cmds.delete()

        leaf = []
        for m in range(19):
            if (m % 3 == 0) or (m % 3 == 1):
                leaf.append(f"{PFX}leaf_{i + 1}.e[{m}]")
        cmds.polyExtrudeEdge(leaf)
        cmds.scale(3, 1, 3)
        cmds.move(0, 0.5, 0, leaf, relative=True)

        # scale leaf to fit
        cmds.select(f"{PFX}leaf_" + str(i + 1))
        cmds.scale(0.3, 0.3, 0.3)
        cmds.DeleteHistory()
        cmds.FreezeTransformations()

        # parent leaf to strawberry
        cmds.parent(f"{PFX}leaf_" + str(i + 1), f"{PFX}ball_" + str(i + 1))

        # create handles
        cmds.polyTorus(n=f"{PFX}handle_" + str(i + 1), sr=.51, sx=30)
        cmds.select(f"{PFX}handle_" + str(i + 1))
        cmds.rotate(90, 90, 0)
        cmds.move(-5 + i * 2.6, 4.12, 0)
        cmds.scale(0.2, 0.2, 0.2)
        cmds.DeleteHistory()
        cmds.FreezeTransformations()

        # parent handles to balls
        cmds.parent(f"{PFX}handle_" + str(i + 1), f"{PFX}ball_" + str(i + 1))

        # create and apply shader
        chrome = cmds.shadingNode("aiStandardSurface", n=f"{PFX}chromeShd", asShader=True)
        cmds.select(f"{PFX}ball_" + str(i + 1))
        cmds.hyperShade(assign=chrome)
        cmds.setAttr(chrome + ".metalness", 1)
        cmds.setAttr(chrome + ".specularRoughness", .14)
        cmds.setAttr(chrome + ".baseColor", 1, 0, 0)

        chrome_leaves = cmds.shadingNode("aiStandardSurface", n=f"{PFX}chromeShdLeaf", asShader=True)
        cmds.select(f"{PFX}leaf_" + str(i + 1), f"{PFX}handle_" + str(i + 1))
        cmds.hyperShade(assign=chrome_leaves)
        cmds.setAttr(chrome_leaves + ".metalness", 1)
        cmds.setAttr(chrome_leaves + ".specularRoughness", .14)
        cmds.setAttr(chrome_leaves + ".baseColor", 0, 1, 0)

    # create supports
    rings = cmds.group(empty=True, n=f"{PFX}ring_GRP")

    for i in range(5):
        # create string 1
        cmds.polyCylinder(n=f"{PFX}supp_" + str(i + 1), r=0.05, h=8)
        cmds.rotate(35)
        cmds.move(-5 + i * 2.6, 7.3, 2.2)

    for n in range(5, 10):
        # create string 2
        cmds.polyCylinder(n=f"{PFX}supp_" + str(n + 1), r=0.05, h=8)
        cmds.rotate(-215)
        cmds.move(-18 + n * 2.6, 7.3, -2)
        cmds.DeleteHistory()
        cmds.FreezeTransformations()

    for i in range(5):
        # create ring 1
        cmds.polyTorus(n=f"{PFX}ring_" + str(i + 1), sr=.1, sx=30)
        cmds.select(f"{PFX}ring_" + str(i + 1))
        cmds.rotate(90, 90, 0)
        cmds.move(-5 + i * 2.6, 10.34, 4.5)
        cmds.scale(0.3, 0.3, 0.3)
        cmds.DeleteHistory()
        cmds.FreezeTransformations()

    for p in range(5, 10):
        # create ring 2
        cmds.polyTorus(n=f"{PFX}ring_" + str(p + 1), sr=.1, sx=30)
        cmds.select(f"{PFX}ring_" + str(p + 1))
        cmds.rotate(90, 90, 0)
        cmds.move(-18 + p * 2.6, 10.3, -4.55)
        cmds.scale(0.3, 0.3, 0.3)
        cmds.DeleteHistory()
        cmds.FreezeTransformations()

    # parent and group each strand
    for o in range(10):
        cmds.parent(f"{PFX}ring_" + str(o + 1), rings)

    # parenting each string together
    cmds.parent(f"{PFX}supp_1", f"{PFX}supp_6")
    cmds.parent(f"{PFX}supp_2", f"{PFX}supp_7")
    cmds.parent(f"{PFX}supp_3", f"{PFX}supp_8")
    cmds.parent(f"{PFX}supp_4", f"{PFX}supp_9")
    cmds.parent(f"{PFX}supp_5", f"{PFX}supp_10")

    # parenting all strings to balls
    cmds.parent(f"{PFX}supp_6", f"{PFX}ball_1")
    cmds.parent(f"{PFX}supp_7", f"{PFX}ball_2")
    cmds.parent(f"{PFX}supp_8", f"{PFX}ball_3")
    cmds.parent(f"{PFX}supp_9", f"{PFX}ball_4")
    cmds.parent(f"{PFX}supp_10", f"{PFX}ball_5")

    for pivot in range(5):
        # move pivot point balls
        cmds.xform(f"{PFX}ball_" + str(pivot + 1), piv=(0, 7.2, 0), r=True)

    # create and apply shader
    supp_obj_color = cmds.shadingNode('aiStandardSurface', n=f"{PFX}suppShd", asShader=True)
    cmds.setAttr(supp_obj_color + ".metalness", .7)
    cmds.setAttr(supp_obj_color + ".specularRoughness", .14)
    cmds.setAttr(supp_obj_color + ".baseColor", .3, 1, .3)

    for d in range(10):
        cmds.select(f"{PFX}supp_" + str(d + 1))
        cmds.hyperShade(assign=supp_obj_color)
        cmds.select(f"{PFX}ring_" + str(d + 1))
        cmds.hyperShade(assign=supp_obj_color)

    # group balls
    curr = cmds.group(f"{PFX}ball_1", f"{PFX}ball_2", f"{PFX}ball_3",
                      f"{PFX}ball_4", f"{PFX}ball_5", n=f"{PFX}ball_GRP")

    return curr


def table():
    # create model
    curr = cmds.polyCube(n=f"{PFX}table")
    cmds.scale(150, 1, 50)
    cmds.move(0, -1, -2)

    cmds.group(f"{PFX}table", n=f"{PFX}table_GRP")

    # add texture
    table_color = cmds.shadingNode('aiStandardSurface', n=f"{PFX}tableShd", asShader=True)
    cmds.setAttr(table_color + ".baseColor", .05, .05, .05)
    cmds.setAttr(table_color + ".specular", .2)
    cmds.setAttr(table_color + ".specularRoughness", .15)
    cmds.select(curr)
    cmds.hyperShade(assign=table_color)

    return curr


def lights():
    # create sky
    skydome = cmds.shadingNode('aiSkyDomeLight', asLight=True)
    cmds.setAttr(skydome + ".intensity", .5)
    cmds.rename(skydome, f"{PFX}sky")

    # create lights
    cmds.directionalLight(n=f"{PFX}dirLight1")  # light 1
    cmds.rotate(-48, 15, 25.5)
    cmds.setAttr(f"{PFX}dirLight1.color", 1, .8, .6)
    cmds.setAttr(f"{PFX}dirLight1.intensity", 2)

    cmds.directionalLight(n=f"{PFX}dirLight2")  # light 2
    cmds.rotate(-19, -207, -.7)
    cmds.setAttr(f"{PFX}dirLight2.color", 0.3, 0.5, 0.54)
    cmds.setAttr(f"{PFX}dirLight2.intensity", 3)

    curr = cmds.group(f"{PFX}sky", f"{PFX}dirLight1", f"{PFX}dirLight2", n=f"{PFX}light_GRP")

    return curr


def camera():
    # create camera
    curr = cmds.camera(n=f"{PFX}camera")
    cmds.move(15, 9.5, -29)
    cmds.rotate(-9.6, 154, 0)
    cmds.lookThru(curr)

    return curr


def expressions():
    # animate everything
    cmds.expression(object=f"{PFX}ball_5", s=f"{PFX}ball_5.rotateZ = clamp(0,40,sin(time*5)*40)")
    cmds.expression(object=f"{PFX}ball_1", s=PFX + '''ball_1.rotateZ = clamp(-40,0,sin(time*5)*40)''')
    cmds.expression(object=f"{PFX}ball_4", s=f"{PFX}ball_4.rotateZ = clamp(.5,3,sin(time*5)*3)")
    cmds.expression(object=f"{PFX}ball_2", s=PFX + '''ball_2.rotateZ = clamp(-3,-.5,sin(time*5)*3)''')
    cmds.expression(object=f"{PFX}ball_3", s=f"{PFX}ball_3.rotateZ = clamp(-.5,.5,sin(time*5)*.5)")


def main():
    # removes anything that begins with PFX
    if cmds.objExists(PFX + "*"):
        cmds.delete(PFX + "*")

    # run everything
    table()
    base()
    beams()
    balls()
    lights()
    camera()

    expressions()

    # cleanup
    cmds.select(PFX + "*")
    cmds.DeleteHistory()
    cmds.FreezeTransformations()

    cmds.select(clear=True)

    print("Done!")


main()
