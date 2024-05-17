<?php

use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Validator\Constraints\NotBlank;

class MailFormType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('theme', TextType::class, [
                'constraints' => [
                    new NotBlank(['message' => 'Pole tematu nie może być puste.']),
                ],
            ])
            ->add('contents', TextareaType::class, [
                'constraints' => [
                    new NotBlank(['message' => 'Pole treści nie może być puste.']),
                ],
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            // Tutaj możesz dodać opcje, jeśli są potrzebne
        ]);
    }
}
