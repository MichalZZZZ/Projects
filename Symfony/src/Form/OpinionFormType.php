<?php

namespace App\Form;

use App\Entity\OpinionSeller;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Validator\Constraints\NotBlank;

class OpinionFormType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('scale', ChoiceType::class, [
                'label' => 'Ocena',
                'choices' => [
                    '5' => 5,
                    '4' => 4,
                    '3' => 3,
                    '2' => 2,
                    '1' => 1,
                ],
                'expanded' => true,
                'constraints' => [
                    new NotBlank(),
                ]
            ])
            ->add('description', TextareaType::class, [
                'label' => 'Opis opinii',
                'attr' => ['placeholder' => 'Napisz swoją opinię...'],
            ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => OpinionSeller::class,
        ]);
    }
}
